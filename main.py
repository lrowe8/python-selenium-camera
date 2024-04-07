import chromedriver_autoinstaller
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def video_devices_webpage(path: Path) -> None:
    with open(path, 'w') as f:
        f.write(
            '''
            <!DOCTYPE html>

            <html style="cursor: none;">
            <head>
                <script>
                    if (!navigator.mediaDevices?.enumerateDevices) {
                        console.log("enumerateDevices() not supported.");
                    } else {
                        // List cameras and microphones.
                        navigator.mediaDevices.getUserMedia({ video: true });
                        navigator.mediaDevices
                            .enumerateDevices()
                            .then((devices) => {
                                let filteredDevices = devices.filter((device => device.kind === "videoinput"));

                                filteredDevices.forEach((device) => {
                                    console.log(`${device.kind}: ${device.label} id = ${device.deviceId}`);
                            });
                        })
                        .catch((err) => {
                            console.error(`${err.name}: ${err.message}`);
                        });
                    }
                </script>
            </head>
            <body style="background: black; display:flex; margin:0px;">
            </body>
            </html>
            '''
        )

if __name__ == '__main__':
    cwd = Path(__file__).parent
    file_name = "temp.html"

    video_devices_webpage(cwd / file_name)
    chrome_driver_path = chromedriver_autoinstaller.install(cwd=True)

    service = Service(chrome_driver_path)

    options = Options()
    options.add_argument("--autoplay-policy=no-user-gesture-required")
    options.add_argument("start-maximized")
    options.add_argument("--auto-open-devtools-for-tabs")
    # This is the line that automatically allows media device discovery
    options.add_argument("--use-fake-ui-for-media-stream") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"file://{cwd / file_name}")

    input("Press Enter to exit")

    try:
        driver.close()
    except Exception:
        pass