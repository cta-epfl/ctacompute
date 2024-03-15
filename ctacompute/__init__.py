from textwrap import dedent
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
        r = self.client.submit(script_str=dedent(f"""
                               #!/bin/bash                                                 
                               #SBATCH --account=cta02
                               #SBATCH -C mc
                                                 
                               set -xe    
                                                 
                               curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
                               bash Miniforge3-$(uname)-$(uname -m).sh -b -f -p /scratch/snx3000/{self.username}/miniforge3
                                                 
                               . /scratch/snx3000/{self.username}/miniforge3/bin/activate
                                                 
                               curl -O https://gammapy.org/download/install/gammapy-1.2-environment.yml
                               mamba env create -f gammapy-1.2-environment.yml
                                                 
                               """[1:]), machine="daint")
        print(r)


    def test_env(self):
        r = self.client.submit(script_str=dedent(f"""
                               #!/bin/bash                                                 
                               #SBATCH --account=cta02
                               #SBATCH -C mc
                                                 
                               hostname
                                                 
                               pwd
                                                 
                               ls -lort

                               . /scratch/snx3000/{self.username}/miniforge3/bin/activate
                                                 
                               mamba activate gammapy-1.2
                                                 
                               """[1:]), machine="daint")
        print(r)        