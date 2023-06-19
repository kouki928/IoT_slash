<html lang="en">

  <head>

    <meta charset="utf-8" />

    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>

    <script

      src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"

      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"

      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"

      crossorigin="anonymous"

    ></script>


    <link

      rel="stylesheet"

      href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css"

    />

  </head>

  <body>

    <h3 id="bploading" style="text-align:center;">LOADING...</h3>

    <div id="OBNIZ_OUTPUT"></div>

    <br />

    

    <script

      src="https://unpkg.com/obniz@latest/obniz.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/iothome/index.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/airobot/index.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/ui/index.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/ai/howler2.1.2/howler.js"

      crossorigin="anonymous"

    ></script>

    

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/ai/opencv3.4/opencv.js"

      crossorigin="anonymous"

    ></script>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@3.3.0"></script>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet@2.1.0"></script>

    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/posenet@2.2.2"></script>

    

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/ai/clmtrackr/clmtrackr.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/ai/clmtrackr/emotion_classifier.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/ai/clmtrackr/emotionmodel.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/ai/clmtrackr/model_pca_20_svm.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/ai/index.js"

      crossorigin="anonymous"

    ></script>

    <script

      src="https://unpkg.com/obniz-parts-kits@0.16.0/storage/index.js"

      crossorigin="anonymous"

    ></script>




    

    <script>

        $("#bploading").text("RUNNING...");

        (async function(){

            var obniz, hc_sr04, keyestudio_trafficlight, label;
            let flag = true;

            

            

            obniz = new Obniz('OBNIZ_ID_HERE');

            await obniz.connectWait();

            hc_sr04 = obniz.wired("HC-SR04",{"gnd":0, "echo":1, "trigger":2, "vcc":3});

            keyestudio_trafficlight = obniz.wired("Keyestudio_TrafficLight",{"gnd":4, "green":5, "yellow":6, "red":7});

            label = new ObnizUI.Label('label');

            while (true) {

            await ObnizUI.Util.wait(0);

            label.setText(((await hc_sr04.measureWait())));

            if ((await hc_sr04.measureWait()) <= 750) {

                keyestudio_trafficlight.red.off();

                await obniz.wait(100);

                keyestudio_trafficlight.yellow.off();

                await obniz.wait(100);

                while ((await hc_sr04.measureWait()) <= 750) {

                await ObnizUI.Util.wait(0);

                keyestudio_trafficlight.green.on();

                await obniz.wait(100);

                keyestudio_trafficlight.green.off();

                await obniz.wait(100);

                }

            } else if ((await hc_sr04.measureWait()) <= 500) {

                keyestudio_trafficlight.green.off();

                await obniz.wait(100);

                keyestudio_trafficlight.red.off();

                await obniz.wait(100);

                while ((await hc_sr04.measureWait()) <= 500) {

                await ObnizUI.Util.wait(0);

                keyestudio_trafficlight.yellow.on();

                await obniz.wait(100);

                keyestudio_trafficlight.yellow.off();

                await obniz.wait(100);

                }

            } else if ((await hc_sr04.measureWait()) <= 150) {

                keyestudio_trafficlight.green.off();

                keyestudio_trafficlight.yellow.off();

                if (flag) {
                    fetch("url",{
                        method  : "POST",
                        headers : {
                        "Content-Type" : "application/json",
                        },
                        body: JSON.stringify({
                            "id" : id,
                            "key" : key,
                        })
                    }).then(() => {
                        flag = false;
                    })
                }

                while ((await hc_sr04.measureWait()) <= 150) {

                await ObnizUI.Util.wait(0);

                keyestudio_trafficlight.red.on();

                await obniz.wait(100);

                keyestudio_trafficlight.red.off();

                await obniz.wait(100);

                }

            }

            if ((await hc_sr04.measureWait()) <= 50) {

                keyestudio_trafficlight.green.off();

                keyestudio_trafficlight.yellow.off();

                while ((await hc_sr04.measureWait()) <= 50) {

                await ObnizUI.Util.wait(0);

                keyestudio_trafficlight.red.on();

                await obniz.wait(50);

                keyestudio_trafficlight.red.off();

                await obniz.wait(50);

                }

            }

            }

        

        })();

    

    </script>

  </body>

</html>