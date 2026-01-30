Creating a complete Python program for an eco-footprint dashboard involves several steps, such as setting up a web framework, creating a frontend for user interaction, calculating the carbon footprint based on user inputs, and visualizing the data. For simplicity, I will use Flask as the web framework and Matplotlib for creating visualizations. This example will be a basic dashboard with minimal functionality for demonstration purposes.

1. **Set up the environment**: You need to have Flask, Matplotlib, and some basic HTML/CSS for the frontend. You can install Flask and Matplotlib using pip:

    ```bash
    pip install Flask matplotlib
    ```

2. **Create the project files**: The project structure might look like this:

    ```
    eco_footprint_dashboard/
    ├── app.py
    ├── templates/
    │   ├── index.html
    │   └── result.html
    ├── static/
    │   └── style.css
    ```

3. **Implement the Python program**:

    - **app.py**: This is the main application file.

    ```python
    from flask import Flask, render_template, request, redirect, url_for
    import matplotlib.pyplot as plt
    import io
    import base64
    import os

    # Initialize the Flask application
    app = Flask(__name__)

    # Helper function to calculate carbon footprint
    def calculate_footprint(data):
        try:
            transport = float(data.get('transport', 0))
            electricity = float(data.get('electricity', 0))
            waste = float(data.get('waste', 0))
            total = transport + electricity + waste
            return (transport, electricity, waste, total)
        except (ValueError, TypeError) as e:
            print(f"Error in calculating footprint: {e}")
            return None

    # Route for the home page
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            result = calculate_footprint(request.form)
            if result is None:
                return render_template('index.html', error="Invalid input values.")
            
            # Redirect to the result page
            return redirect(url_for('result', transport=result[0], electricity=result[1], waste=result[2], total=result[3]))
        return render_template('index.html')

    # Route for the result page
    @app.route('/result')
    def result():
        try:
            transport = float(request.args.get('transport', 0))
            electricity = float(request.args.get('electricity', 0))
            waste = float(request.args.get('waste', 0))
            total = float(request.args.get('total', 0))

            # Create a bar chart
            plt.figure(figsize=(6, 4))
            categories = ['Transport', 'Electricity', 'Waste']
            values = [transport, electricity, waste]
            plt.bar(categories, values, color=['blue', 'green', 'red'])
            plt.title('Carbon Footprint Breakdown')
            plt.xlabel('Category')
            plt.ylabel('Carbon Footprint (in CO2e)')

            # Save the plot to a byte stream
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            return render_template('result.html', plot_url=plot_url, total=total)
        except Exception as e:
            print(f"Error in generating result: {e}")
            return render_template('index.html', error="Error in generating the result.")

    # Start the Flask server
    if __name__ == '__main__':
        app.run(debug=True)
    ```

    - **templates/index.html**: The homepage with a form for input.

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        <title>Eco Footprint Dashboard</title>
    </head>
    <body>
        <h1>Eco Footprint Dashboard</h1>
        <form method="POST">
            <label for="transport">Transport (in CO2e):</label>
            <input type="number" step="any" name="transport" required><br>

            <label for="electricity">Electricity (in CO2e):</label>
            <input type="number" step="any" name="electricity" required><br>

            <label for="waste">Waste (in CO2e):</label>
            <input type="number" step="any" name="waste" required><br>

            <button type="submit">Calculate</button>
        </form>
        {% if error %}
        <p style="color: red;">{{ error }}</p>
        {% endif %}
    </body>
    </html>
    ```

    - **templates/result.html**: Page to display results and graph.

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        <title>Results - Eco Footprint</title>
    </head>
    <body>
        <h1>Carbon Footprint Results</h1>
        <img src="data:image/png;base64,{{ plot_url }}" alt="Carbon Footprint Chart"/><br>
        <p>Total Carbon Footprint: {{ total }} CO2e</p>
        <a href="{{ url_for('index') }}">Back to Home</a>
    </body>
    </html>
    ```

    - **static/style.css**: Simple styling for the dashboard.

    ```css
    body {
        font-family: Arial, sans-serif;
        margin: 20px;
        padding: 0;
    }

    h1 {
        color: #333;
    }

    form {
        margin-bottom: 20px;
    }

    label {
        display: block;
        margin-bottom: 5px;
    }

    input[type="number"] {
        padding: 5px;
        margin-bottom: 10px;
        width: 100%;
        max-width: 300px;
    }

    button {
        padding: 7px 15px;
        background-color: #5cb85c;
        color: #fff;
        border: none;
        cursor: pointer;
    }

    button:hover {
        background-color: #4cae4c;
    }
    ```

4. **Run the application**: Make sure you're in the `eco_footprint_dashboard` directory and run the app using:

    ```bash
    python app.py
    ```

Navigate to `http://127.0.0.1:5000` in your web browser to interact with the dashboard.

This basic setup helps you understand how to create a simple web application for calculating and displaying carbon footprints. You can expand this by adding user authentication, saving data to a database, or integrating more sophisticated visualization tools like Plotly or Chart.js for enhanced interactivity.