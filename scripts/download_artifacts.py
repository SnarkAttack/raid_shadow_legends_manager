
from raidtoolkit import RaidToolkitClient
import asyncio

async def main():

        print("Starting to download artifacts")
        client = RaidToolkitClient()
        client.connect()

        print("Client connected")
        
        print("Fetching accounts")
        accounts = await client.AccountApi.get_accounts()
        print(accounts)
        accounts = [a for a in accounts if a['name'] == "SnarkAttack"]

        if len(accounts) == 0:
            raise ValueError("No account found with that name")
        else:
            account = accounts[0]

        artifacts = await client.AccountApi.get_artifacts(account['id'])

        client.close()

        for artifact_json in artifacts:
            print(artifact_json)
    
if __name__ == "__main__":
    asyncio.run(main())
