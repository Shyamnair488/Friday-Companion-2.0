import subprocess

from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template included in the Python code
html_template = '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Interactive Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            
        }

        button {
            padding: 15px 30px;
            font-size: 18px;
            background-color: rgba(255, 255, 255, 0.7);
            color: white;
            border: none;
          

        button:hover {
            background-color: #45a049; /* Hover color */
        }

        .output-box {
            width: 80%;
           
        }
    </style>
</head>

<body>
    <h1 style="color: white;"><i><b>Friday Assistant</b></i></h1>
    <button onclick="executeCode()">Execute Code</button>
    
                .then(data => {
                    const outputBox = document.getElementById('outputBox');
                    outputBox.textContent = data; // Display the returned data in the output box
                })
                .catch(error => console.error(error));
        }
    </script>
</body>

</html>
'''

@app.route('/')
def index():
    return render_template_string(html_template)

@
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)