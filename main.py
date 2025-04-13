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
    logic.matrix.clear()
    logic.system.clear()
    logic.gauss_steps.clear()
    logic.main_vars.clear()
    logic.sec_vars.clear()
    logic.variables_dict.clear()
    logic.vars_list.clear()
    logic.steps.clear()
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
    print(logic.vars_list)
    return render_template('rezultat.html',
                           matrix = logic.matrix,
                           matrices = logic.gauss_steps,
                           matrix_type = logic.matrix_type,
                           main_vars = logic.main_vars,
                           sec_vars = logic.sec_vars,
                           vars_list = logic.vars_list,
                           var_sol = logic.variables_dict,
                           steps = logic.steps)

if __name__ == "__main__":
    app.run(debug=True)

