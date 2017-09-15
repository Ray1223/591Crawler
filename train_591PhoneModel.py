#============================================================================

def transform_photo_to_array(openFilePath):
    import matplotlib.pyplot as plt
    import PIL
    from PIL import Image
    import numpy
    import os
    digits = []
    labels = []
    basewidth = 150
    fig = plt.figure(figsize=(20, 20))
    cnt = 0
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)
    # 將準備訓練的1-10數字圖檔Load進記憶體
    for i in range(0, 10):
        for img in os.listdir(openFilePath + '{}/'.format(i)):
            pil_image = PIL.Image.open(openFilePath + '{}/{}'.format(i, img)).convert('L')
            # 將分割後的數字讀到記憶體中
            wpercent = (basewidth / float(pil_image.size[0]))
            hsize = int((float(pil_image.size[1]) * float(wpercent)))
            img = pil_image.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
            # 根據寬跟高resize

            ax = fig.add_subplot(10, 30, cnt + 1, xticks=[], yticks=[])
            # 200張圖
            ax.imshow(img, cmap=plt.cm.binary, interpolation='nearest')
            ax.text(0, 7, str(i), color="red", fontsize=20)
            cnt = cnt + 1

            digits.append([pixel for pixel in iter(img.getdata())])
            labels.append(i)
            # 轉成一維list

    return (digits,labels)


def check_photo_to_array(digits):
    import numpy
    digit_ary = numpy.array(digits)
    return digit_ary

#圖太大會需要正規化
def scaler_photoArray(digit_ary):
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(digit_ary)
    X_scaled = scaler.transform(digit_ary)
    return X_scaled


#類神經網路MLP分類器
def train_phone_model(X_scaled, savePklPath, labels):
    from sklearn.neural_network import MLPClassifier
    from sklearn.externals import joblib
    import numpy

    mlp = MLPClassifier(hidden_layer_sizes=(30, 30, 30), activation='logistic', max_iter=1500)
    mlp.fit(X_scaled, labels)
    #save into pkl model
    joblib.dump(mlp, savePklPath)
    #train set to asscess the performance of test set
    predicted = mlp.predict(X_scaled)
    target = numpy.array(labels)
    ary = (predicted == target)
    accuracy = str((numpy.sum(ary)/numpy.size(ary))*100)+"%"
    return print("This model accuracy is {}".format(accuracy))



#============================================================================

def main(openFilePath, savePklPath):

    try:
        main_digits = transform_photo_to_array(openFilePath)
        main_digit_ary = check_photo_to_array(main_digits[0])
        main_X_scaled = scaler_photoArray(main_digit_ary)
        train_phone_model(main_X_scaled, savePklPath, main_digits[1])

    except Exception as e:
        print(e)
    print("finished training 591 model!")


if __name__ == "__main__":
    openFilePath = "./number/"
    savePklPath = openFilePath+"591test.pkl"
    main(openFilePath, savePklPath)