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

    def list_files(self):
        total_size = 0
        for i, file_entry in enumerate(client.list_files('daint', '/scratch/snx3000/vsavchen/sdc-simulations/MAKE_SDC/output/products_SDC/Events/')):
            print(f"{i} ", end="")
            for k, v in file_entry.items():
                print(f"{k}:{v} ", end="")
            print("")
            total_size += int(file_entry['size'])

        print("total_size", total_size/1024/1024/1024, "GiB")
