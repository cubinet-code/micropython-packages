import time
import iotmanager
import uasyncio

# Init Manager
iot1 = iotmanager.IotManager(
    use_css=True,
    title="IoT Demo Controller",
    ota_url="http://10.1.1.10:8080/micropython.bin",
    debug=True,
)

# Add a custom config key to manager. This will be persisted.
iot1.config_add(
    {
        "60_CUSTOM_CONFIG": "Counter",
    }
)

# Add Demo Data to Manager
for i in range(5):
    iot1.data[f"Key {i}"] = f"{i}"


# Demo Class - Task to run in the background needs to be a non-blocking asyncio co-routine
class Alive:
    # Method to run must be a async co-routine
    async def run(self):
        i = 0

        # Get a custom config value from manager
        counter_key_name = iot1.config.get("60_CUSTOM_CONFIG")
        while 1:
            print("Increment Counter")
            # Adds dynamic data to the manager for display
            iot1.data[counter_key_name] = f"{i}"
            iot1.data["gmt_time"] = time.gmtime()
            i += 1
            # Ensures that the method yields time to manager and other running tasks
            await uasyncio.sleep(3)


# Add task to manager
iot1.add_task(Alive().run())

# Start Manager, code after this line will not be executed anymore
iot1.run()
