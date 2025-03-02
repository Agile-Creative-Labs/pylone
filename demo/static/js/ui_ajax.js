/**
 * 
 * 
 * you can use it in any template that extends base.html.
 * {% extends "base.html" %}

{% block content %}
    <h1>AJAX Demo</h1>
    <button id="get-data">Get Data</button>
    <button id="post-data">Post Data</button>
    <p id="response-message"></p>

    <script>
        $(document).ready(function() {
            // GET Request Example
            $("#get-data").click(function() {
                ajaxHelper.get("/ajax-demo", {
                    success: (response) => {
                        $("#response-message").text(response.message);
                    },
                    error: (xhr, status, err) => {
                        $("#response-message").text("Error: " + err);
                    },
                });
            });

            // POST Request Example
            $("#post-data").click(function() {
                ajaxHelper.post("/ajax-demo", { name: "John", age: 30 }, {
                    success: (response) => {
                        $("#response-message").text(response.message);
                    },
                    error: (xhr, status, err) => {
                        $("#response-message").text("Error: " + err);
                    },
                });
            });
        });
    </script>
{% endblock %}
 */
class AjaxHelper 
{
    constructor(baseUrl = "") 
    {
        this.baseUrl = baseUrl;
    }

    get(url, options = {}) 
    {
        this._request("GET", url, null, options);
    }

    post(url, data, options = {}) 
    {
        this._request("POST", url, data, options);
    }

    _request(method, url, data, options) 
    {
        const { success, error, headers } = options;
        // Show loading indicator
        this._showLoading();

        $.ajax({
            url: this.baseUrl + url,
            method: method,
            data: method === "GET" ? data : JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            headers: headers,
                    success: (response) => {
                        this._hideLoading();
                        if (success) success(response);
                    },
                    error: (xhr, status, err) => {
                        this._hideLoading();
                        if (error) error(xhr, status, err);
                        else this._handleError(xhr, status, err);
                    },
        });
    }

    _showLoading() 
    {
        console.log("Loading...");
        // Add your loading indicator logic here
    }

    _hideLoading() 
    {
        console.log("Loading complete.");
        // Add your loading indicator logic here
    }

    _handleError(xhr, status, err) 
    {
        console.error("AJAX Error:", status, err);
                alert("An error occurred. Please try again.");
    }
}

// Initialize the AjaxHelper with your base URL
const ajaxHelper = new AjaxHelper("http://127.0.0.1:8000");
 