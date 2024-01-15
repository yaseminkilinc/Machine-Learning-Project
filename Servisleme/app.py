import streamlit as st
import pandas as pd 
import numpy as np
import joblib
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import seaborn as sns


# Ana fonksiyon, Streamlit uygulamasını başlatır
def main():
    
    # Uygulama arka plan rengini ayarlayan fonksiyon
    set_background_color("#E6ECF0")

    # Yan menüdeki navigasyon seçenekleri
    st.sidebar.title('Streamlit ile Machine Learning Uygulaması')
    selected_page = st.sidebar.selectbox('Sayfa seçiniz.', ["Giriş Ekranı", "Tahmin Yap", "İstatistik Görüntüle", "Hakkında"])

    # Seçilen sayfaya göre işlemler
    if selected_page == "Giriş Ekranı":
        image = Image.open(r'C:\Users\YASEMİN\Desktop\212803043_Yasemin_Kılınç_MakineProje\Servisleme\buzdolabi1.png')
        st.image(image, use_column_width=True)
        st.title('Streamlit Uygulamasına Hoşgeldiniz!')

        st.markdown(
            """
            Bu proje makine öğrenmesi uygulamalarının web ortamında streamlit
            kullanılarak yayınlanmasına örnek olarak geliştirilmiştir. Bir e-ticaret sitesi üzerinden 696 adet buzdolabı verileri çekilmiş
            ve incelenmiştir. Bu veriler kullanılarak makine öğrenmesi modelleri eğitilmiş ve projeye dahil edilmiştir.
            
            """)
        st.info("Tahmin yapmak, istatistikleri görüntülemek ve proje hakkında daha fazla bilgi edinmek için sol tarafta bulunan menüyü kullanınız.")
        
    # Tahminleri yapacak fonksiyonu çağır
    if selected_page == "Tahmin Yap":
        predict()
    
    # İstatistikleri gösterecek fonksiyonu çağır
    if selected_page == "İstatistik Görüntüle":
        eda() 
    
    # Geliştirici hakkında bilgi gösteren fonksiyonu çağır
    if selected_page == "Hakkında":
        about() 
    
# Arka plan rengini ayarlayan fonksiyon
def set_background_color(color):
    if color.startswith("#"):
        color_code = color
    else:
        color_code = "#FFFFFF"  # Geçersiz renk durumunda varsayılan olarak beyaz kullanılır
    script = f"""
    <style>
    .stApp {{
        background-color: {color_code};
    }}
    </style>
    """
    st.markdown(script, unsafe_allow_html=True)

# Geliştirici hakkında bilgi gösteren fonksiyon
def about():
    st.title('Geliştirici Bilgileri')
    st.subheader('Github Adresi : [Yasemin KILINÇ](https://github.com/yaseminkilinc/)')
    st.subheader('Linkedin Adresi : [Yasemin KILINÇ](https://www.linkedin.com/in/yasemin-k%C4%B1l%C4%B1n%C3%A7-44553a226/)')
    st.subheader('Mail Adresi : yasemin.klnc26@gmail.com')

# Verilerden istatistik gösteren fonksiyon
def eda():
    st.title('İstatistikler')

    data = pd.read_excel("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Veri_Toplama/veri_on_isleme.xlsx")

    st.header("Bütün Veriler")
    st.dataframe(data)

    plt.figure(figsize=(16, 16))
    plt.subplot(2, 1, 1)
    sns.countplot(x='Markalar', data=data, order=data['Markalar'].value_counts().index)
    plt.xticks(rotation=90)
    plt.xlabel("Marka Adı")
    plt.ylabel("Sayıları")
    st.header("Markaların Sıralaması")
    st.pyplot(fig=plt)

    plt.figure(figsize=(16, 16))
    plt.subplot(2, 1, 1)
    sns.countplot(x='Garanti_Suresi', data=data, order=data['Garanti_Suresi'].value_counts().index)
    plt.xlabel("Garanti_Suresi")
    plt.ylabel("Sayıları")
    plt.xticks(rotation=90)

    st.header("Garanti Süresi Sıralaması")
    st.pyplot(fig=plt)


# Tahmin yapmak için kullanılan fonksiyon
def predict():

    # Tahmin için verileri yükle
    markalar = load_data()
    buzluk_tipi = load_data1()
    dondurucu_yeri = load_data2()
    dondurucu_ozelligi = load_data3()
    enerji_sinifi = load_data4()
    tip = load_data5()
    ucretsiz_kurulum_var_mi = load_data6()

    st.title('Merhaba, Streamlit!')
    # Kullanıcıdan seçim yapmasını isteyen alanlar
    selected_brand = marka_index(markalar, st.selectbox('Marka Seçiniz:', markalar))
    selected_buzluk_tipi = buzluk_tipi_index(buzluk_tipi, st.selectbox('Buzluk Tipi Seçiniz:', buzluk_tipi))
    selected_dondurucu_yeri = dondurucu_yeri_index(dondurucu_yeri, st.selectbox('Dondurucu Yeri Seçiniz:', dondurucu_yeri))
    selected_dondurucu_ozelligi = dondurucu_ozelligi_index(dondurucu_ozelligi, st.selectbox('Dondurucu Özelliği Seçiniz:', dondurucu_ozelligi))
    selected_enerji_sinifi = enerji_sinifi_index(enerji_sinifi, st.selectbox('Enerji Sınıfı Seçiniz:', enerji_sinifi))
    selected_tip = tip_index(tip, st.selectbox('Tip Seçiniz:', tip))
    selected_ucretsiz_kurulum_var_mi = ucretsiz_kurulum_var_mi_index(ucretsiz_kurulum_var_mi, st.selectbox('Ücretsiz Kurulum Olup Olmayacağını Seçiniz:', ucretsiz_kurulum_var_mi))

    # Sayısal değerler için kaydırma çubukları
    selected_depth = st.slider("Derinlik", min_value=45, max_value=97)
    st.write("Derinlik :" + str(selected_depth) + " cm")
    selected_warranty_period = st.slider("Garanti_Suresi", min_value=2, max_value=7)
    st.write("Garanti_Suresi :" + str(selected_warranty_period) + " yıl")
    selected_total_volume = st.slider("Toplam_Hacim", min_value=90, max_value=601)
    st.write("Toplam_Hacim :" + str(selected_total_volume) + " L")


    # Kullanıcı seçimlerine göre tahmin değeri oluştur
    prediction_value = create_prediction_value(selected_brand, selected_buzluk_tipi, selected_dondurucu_yeri, selected_dondurucu_ozelligi,
                                               selected_enerji_sinifi, selected_tip, selected_ucretsiz_kurulum_var_mi, selected_depth, selected_warranty_period, selected_total_volume)
    prediction_model = load_models("Random Forest")

    # Tahmin yap butonu
    if st.button("Tahmin Yap"):
        result = predict_models(prediction_model, prediction_value)
        # Tahmin sonucunu göster
        if result != None:
            st.success('Tahmin Başarılı')
            st.balloons()
            st.write("Tahmin Edilen Fiyat: " + result + "TL")
        else:
            st.error('Tahmin yaparken hata meydana geldi.!')

# Excel dosyalarından veri yükleme fonksiyonları
def load_data():
    markalar = pd.read_excel("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Veri_Toplama/markalar.xlsx")
    return markalar
def load_data1():
    buzluk_tipi=pd.read_excel("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Veri_Toplama/Buzluk_Tipi.xlsx")
    return buzluk_tipi
def load_data2():
    dondurucu_yeri=pd.read_excel("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Veri_Toplama/Dondurucu_Yeri.xlsx")
    return dondurucu_yeri
def load_data3():
    dondurucu_ozelligi=pd.read_excel("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Veri_Toplama/Dondurucu_Ozelligi.xlsx")
    return dondurucu_ozelligi
def load_data4():
    enerji_sinifi=pd.read_excel("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Veri_Toplama/Enerji_Sinifi.xlsx")
    return enerji_sinifi
def load_data5():
    tip=pd.read_excel("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Veri_Toplama/Tip.xlsx")
    return tip
def load_data6():
    ucretsiz_kurulum_var_mi=pd.read_excel("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Veri_Toplama/Ucretsiz_Kurulum_Var_Mi.xlsx")
    return ucretsiz_kurulum_var_mi

# Makine öğrenmesi modellerini dosyalardan yükleme fonksiyonu
def load_models(modelName):
    if modelName == "Random Forest":
        rf_model = joblib.load("C:/Users/YASEMİN/Desktop/212803043_Yasemin_Kılınç_MakineProje/Algoritmalar/random_forest_regression_model.pkl")
        return rf_model
    else:
        st.write("Model yüklenirken hata meydana geldi.!")
        return 0

# Yüklü verilerden seçilen öğelerin indekslerini almak için kullanılan fonksiyonlar
def marka_index(markalar, Markalar):
    index = int(markalar[markalar["Markalar"] == Markalar].index.values)
    return index
def buzluk_tipi_index(buzluk_tipi, Buzluk_Tipi):
    index = int(buzluk_tipi[buzluk_tipi["Buzluk_Tipi"] == Buzluk_Tipi].index.values[0])
    return index

def dondurucu_yeri_index(dondurucu_yeri, Dondurucu_Yeri):
    index = int(dondurucu_yeri[dondurucu_yeri["Dondurucu_Yeri"] == Dondurucu_Yeri].index.values[0])
    return index

def dondurucu_ozelligi_index(dondurucu_ozelligi, Dondurucu_Ozelligi):
    index = int(dondurucu_ozelligi[dondurucu_ozelligi["Dondurucu_Ozelligi"] == Dondurucu_Ozelligi].index.values[0])
    return index

def enerji_sinifi_index(enerji_sinifi,Enerji_Sinifi):
    index = int(enerji_sinifi[enerji_sinifi["Enerji_Sinifi"] == Enerji_Sinifi].index.values[0])
    return index

def tip_index(tip,Tip):
    index = int(tip[tip["Tip"] == Tip].index.values[0])
    return index

def ucretsiz_kurulum_var_mi_index(ucretsiz_kurulum_var_mi,Ucretsiz_Kurulum_Var_Mi):
    index = int(ucretsiz_kurulum_var_mi[ucretsiz_kurulum_var_mi["Ucretsiz_Kurulum_Var_Mi"] == Ucretsiz_Kurulum_Var_Mi].index.values[0])
    return index

# Kullanıcı girişlerine göre tahmin verisi oluşturan fonksiyon
def create_prediction_value(Markalar,Buzluk_Tipi,Derinlik,Dondurucu_Yeri,Dondurucu_Ozelligi,Enerji_Sinifi,Garanti_Suresi,Tip,Toplam_Hacim,Ucretsiz_Kurulum_Var_Mi):
    res = pd.DataFrame(data = 
            {'Markalar':[Markalar],'Buzluk_Tipi':[Buzluk_Tipi],'Derinlik':[Derinlik],
             'Dondurucu_Yeri':[Dondurucu_Yeri],'Dondurucu_Ozelligi':[Dondurucu_Ozelligi],
              'Enerji_Sinifi':[Enerji_Sinifi],'Garanti_Suresi':[Garanti_Suresi],'Tip':[Tip],'Toplam_Hacim':[Toplam_Hacim],'Ucretsiz_Kurulum_Var_Mi':[Ucretsiz_Kurulum_Var_Mi]})
    return res

# Yüklenen model ve giriş verisiyle tahmin yapmayı sağlayan fonksiyon
def predict_models(model, res):
    result = str(int(model.predict(res))).strip('[]')
    return result


# Script çalıştığında main fonksiyonunu çalıştır
if __name__ == "__main__":
    main()
