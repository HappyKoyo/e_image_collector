# 概要  
物体認識用の画像を集めるためのパッケージです。  

# 実行方法  
    $ roslaunch realsense_camera r200_nodelet_rgbd.launch  
    ${PKG_ROOT}/darknet$ sh misdetected_image_collector.sh  
realsense_cameraは別パッケージ

# 使い方  
実行をすると、以下のメッセージが表示されます。  

    Press -t- for take the picture  
ここで't'を押すと画像が**image/full_image.png**に保存され、YOLOによる推論が始まります。その後、その結果が**image/result.png**に保存され、誤検出をしていた場合's'を押すことで保存されます。正しく推論できていた場合はそれ以外のキーを入力することでその画像を破棄出来ます。  

# その他  
weightやcfgを変えたい場合は、通常のものと同じ手順で大丈夫です。
