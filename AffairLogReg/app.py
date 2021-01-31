from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def homepage():
    return render_template('Index.html')

@app.route('/predict',methods = ['POST'])
def index():
    if request.method == 'POST':
        try:
            occ_wife = float(request.form['occ_wife'])
            occ_hus = float(request.form['occ_hus'])
            rate_marriage = float(request.form['rate_marriage'])
            age = float(request.form['age'])
            yrs_married = float(request.form['yrs_married'])
            children = float(request.form['children'])
            religious = float(request.form['religious'])
            edu = float(request.form['edu'])

            oc = [1, 0, 0, 0, 0, 0]
            if occ_wife == 2:
                oc[1] = 1
            elif occ_wife == 3:
                oc[2] = 1
            elif occ_wife == 4:
                oc[3] = 1
            elif occ_wife == 5:
                oc[4] = 1
            elif occ_wife == 6:
                oc[5] = 1

            oc_h = [0, 0, 0, 0, 0]
            if occ_hus == 2:
                oc_h[0] = 1
            elif occ_hus == 3:
                oc_h[1] = 1
            elif occ_hus == 4:
                oc_h[2] = 1
            elif occ_hus == 5:
                oc_h[3] = 1
            elif occ_hus == 6:
                oc_h[4] = 1

            scaler = pickle.load(open('CheatScaler.pkl','rb'))
            scaled_data = scaler.transform([[rate_marriage,age,yrs_married,children,religious,edu]])

            data = [oc + oc_h + list(scaled_data[0])]

            model = pickle.load(open('CheatLogR.pkl','rb'))
            pred = model.predict(data)
            res = " "
            if pred == 1:
                res = "Yes, it's an affair"
            elif pred == 0:
                res = "No, not an affair"

            return render_template('Result.html', pred = res)
        except:
            print("Some Error Occured")
    return render_template('Index.html')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
