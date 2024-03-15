from textwrap import dedent
import time
import firecrest as fc
import subprocess



class CTAComputeClient:
    def login(self):
        client_id = subprocess.check_output(["pass", "firecrest-jhtest-id"]).decode().strip()
        client_secret =subprocess.check_output(["pass", "firecrest-jhtest"]).decode().strip()
        token_uri = "https://auth.cscs.ch/auth/realms/firecrest-clients/protocol/openid-connect/token"

        # Setup the client for the specific account
        self.client = fc.Firecrest(
            firecrest_url="https://firecrest.cscs.ch",
            authorization=fc.ClientCredentialsAuth(client_id, client_secret, token_uri)
        )
        print(self.client.all_systems())

        self.username = self.client.whoami()

        print(f"Logged in as {self.username}")

        self.machine = "daint"

    def status(self):
        print(self.client.all_systems())


    def list_files(self):
        total_size = 0
        for i, file_entry in enumerate(self.client.list_files('daint', f'/scratch/snx3000/{self.username}/sdc-simulations/MAKE_SDC/output/products_SDC/Events/')):
            print(f"{i} ", end="")
            for k, v in file_entry.items():
                print(f"{k}:{v} ", end="")
            print("")
            total_size += int(file_entry['size'])

        print("total_size", total_size/1024/1024/1024, "GiB")

    def setup_env(self):
        self.run(dedent(f"""
                        #!/bin/bash                                                 
                        #SBATCH --account=cta02
                        #SBATCH -C mc
                                            
                        set -xe    
                                            
                        curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
                        bash Miniforge3-$(uname)-$(uname -m).sh -b -f -p /scratch/snx3000/{self.username}/miniforge3
                                            
                        . /scratch/snx3000/{self.username}/miniforge3/bin/activate
                                            
                        curl -O https://gammapy.org/download/install/gammapy-1.2-environment.yml
                        mamba env create -f gammapy-1.2-environment.yml
                                            
                        """[1:]), sync=True)
                

    def run(self, script_str, sync=False):
        r = self.client.submit(script_str=script_str, machine=self.machine)
        print(r)        
        job_file_out = r['job_file_out']

        if sync:
            jobid = r['jobid']

            all_completed = False
            while not all_completed:
                r = self.client.poll(machine=self.machine, jobs=[jobid])
                print(r)

                all_completed = True
                for job in r:                    
                    print(job['jobid'], job['state'])
                    if job['state'] != "COMPLETED":                    
                        all_completed = False
                    else:
                        print("job completed!")

                try:
                    r = self.client.view(target_path=job_file_out, machine=self.machine)
                    print(r)
                except fc.FirecrestException as e:
                    print(e)
                    all_completed = False                                

            print(r)
        
    
    def test_env(self):
        self.run(dedent(f"""
                #!/bin/bash                                                 
                #SBATCH --account=cta02
                #SBATCH -C mc
                                    
                hostname
                                    
                pwd
                                    
                ls -lort

                . /scratch/snx3000/{self.username}/miniforge3/bin/activate
                                    
                conda activate gammapy-1.2

                python -c "import gammapy; print(gammapy.__version__)"

                gammapy --version
                                    
                """[1:]), sync=True)