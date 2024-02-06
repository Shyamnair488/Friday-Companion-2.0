from flask import Flask, render_template_string, request
import subprocess

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
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0; /* Change the background color of the webpage */
            background-image: url('https://i.gifer.com/QNBH.gif'); /* Specify the path to your GIF image */
            background-size: cover; /* Adjust the background image size */
            overflow: hidden;
        }

        button {
            padding: 15px 30px;
            font-size: 18px;
            background-color: rgba(255, 255, 255, 0.7);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            margin-bottom: 20px;
        }

        button:hover {
            background-color: #45a049; /* Hover color */
        }

        .output-box {
            width: 80%;
            margin: 20px auto;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
        }
    </style>
</head>

<body>
    <button onclick="executeCode()">Execute Code</button>
    <div class="output-box" id="outputBox"></div> <!-- Output box to display the returned data -->
    <script>
        function executeCode() {
            fetch(`/run_code`) // Replace '/run_code' with your actual endpoint
                .then(response => response.text())
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

@app.route('/run_code', methods=['GET', 'POST'])
def run_code():
    try:
        process = subprocess.Popen(['python', 'C:/Users/shyam/Desktop/Projects/FRIDAY/friday.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            return str(error)
        return output.decode()
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
