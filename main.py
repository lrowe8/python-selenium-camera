import chromedriver_autoinstaller
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def video_devices_webpage(path: Path) -> None:
    with open(path, 'w') as f:
        f.write(
'''
.elementContainer {
    display: flex;
}

.myDiv {
    margin-bottom: 40px;
}

<!DOCTYPE html>

<html style="cursor: none;">
    <head>
        <script type="text/javascript">
            if (!navigator.mediaDevices?.enumerateDevices) {
                console.log("enumerateDevices() not supported.");
            } else {
                // List cameras and microphones.
                navigator.mediaDevices.getUserMedia({ video: true });
                navigator.mediaDevices
                    .enumerateDevices()
                    .then((devices) => {
                        cameraOptions = document.getElementById('cameraOptions')
                        let filteredDevices = devices.filter((device => device.kind === "videoinput"));

                        filteredDevices.forEach((device) => {
                            cameraOptions.options[cameraOptions.options.length] = new Option(device.label.split('(')[0], device.deviceId);
                    });
                })
                .catch((err) => {
                    console.error(`${err.name}: ${err.message}`);
                });
            }

            function startStreaming(source) {
                //Selector for your <video> element
                const video = document.querySelector('#myVidPlayer');
                console.log(source);

                //Core
                window.navigator.mediaDevices.getUserMedia({ video: {deviceId: source} })
                    .then(stream => {
                        console.log(stream);
                        video.srcObject = stream;
                        video.onloadedmetadata = (e) => {
                            video.play();
                        };
                    })
                    .catch( () => {
                        alert('You have give browser the permission to run Webcam and mic ;( ');
                    });
            }
        </script>
    </head>

    <body style="background: black; display:flex; margin:0px;">
        <div class="elementContainer">
            <div class="myDiv">
                <video id="myVidPlayer" width="100%" height="75%" controls muted autoplay></video>
            </div>
            <div class="myDiv">
                <select name="options" id="cameraOptions" onchange="startStreaming(this.value)">
                    <option value="">Make a selection</option>
                </select>
            </div>
        </div>
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