from flask import Flask,render_template,request
import logic
app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home():
    
    return render_template("home.html")

@app.route('/crearematrice', methods=['POST'])
def crearematrice():
    global linia
    logic.system.clear()
    logic.gauss_steps.clear()
    logic.var_type_neg.clear()
    logic.var_type_neg.clear()
    logic.variables_dict.clear()
    linia = request.form.get('linia')
    try:
        linia = int(linia)

    except ValueError:
        return "Valori invalide"
    return render_template('crearematrice.html', linia=linia)



@app.route('/rezultat',methods=['GET','POST'])
def rezultat():
    for i in range(linia):
        logic.system.append(request.form.get(f"matriceaIntrodusa_{i}"))
    logic.main()
    return render_template('rezultat.html',matrices = logic.gauss_steps,matrix_type=logic.matrix_type,var_pos = logic.var_type_pos,var_neg=logic.var_type_neg,var_sol=logic.variables_dict )


if __name__ == "__main__":
    app.run(debug=True)

