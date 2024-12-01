from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import re

app = Flask(__name__)

# Dummy data store for demonstration
data_store = {"product_info": [],"business_value": [],"product_owners_main": [],
                "product_owners": [], "business_owners": [],
                "snowflake_data_sources":[],"other_data_sources": [], "platforms": []
            }

# Helper function for email validation
def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@xyz\.com$", email) is not None

# @app.route("/", methods=["GET", "POST"])
# def step1():
#     if request.method == "POST":
#         # Save Step 1 data into the data_store
#         data_store["product_info"] = {
#             "product_name": request.form.get("product_name", ""),
#             "version": request.form.get("version", ""),
#             "launch_date": request.form.get("launch_date", ""),
#             "status": request.form.get("status", "Active"),
#             "product_properties": request.form.getlist("product_properties"),
#             "retirement_date": request.form.get("retirement_date", "9999-12-31"),
#             "description": request.form.get("description", ""),
#             "risks": request.form.get("risks", ""),
#             "additional_properties": request.form.get("additional_properties", ""),
#             "documentation_url": request.form.get("documentation_url", ""),
#             "repository_url": request.form.get("repository_url", ""),
#             "metrics_dashboard": request.form.get("metrics_dashboard", ""),
#         }
#         data_store["business_value"] = {
#             "decision_making": request.form.get("decision_making", 5),
#             "monetization": request.form.get("monetization", 5),
#             "time_savings": request.form.get("time_savings", 5),
#             "reporting": request.form.get("reporting", 5),
#             "processes": request.form.get("processes", 5),
#             "collaboration": request.form.get("collaboration", 5),
#             "documentation_audits": request.form.get("documentation_audits", 5),
#         }
#         data_store["product_owner_main"] = {
#             "product_owner_name": request.form.get("product_owner_name", ""),
#             "product_owner_zid": request.form.get("product_owner_zid", ""),
#             "product_owner_email": request.form.get("product_owner_email", ""),
#             "valid_from_date": request.form.get("valid_from_date", ""),
#             "valid_to_date": request.form.get("valid_to_date", "9999-12-31"),
#         }

#         return redirect(url_for("step2"))

#     return render_template("step1.html", data_store=data_store)

@app.route("/", methods=["GET", "POST"])
def step1():
    if request.method == "POST":
        # Capture data from the form
        print(request.form.to_dict())
        data_store["product_info"] = {
            "product_name": request.form.get("product_name"),
            "version": request.form.get("version"),
            "launch_date": request.form.get("launch_date"),
            "status": request.form.get("status"),
            "product_properties": request.form.getlist("product_properties"),
            "retirement_date": request.form.get("retirement_date"),
            "description": request.form.get("description"),
            "risks": request.form.get("risks"),
            "additional_properties": request.form.get("additional_properties"),
            "documentation_url": request.form.get("documentation_url"),
            "repository_url": request.form.get("repository_url"),
            "metrics_dashboard": request.form.get("metrics_dashboard"),
        }

        data_store["business_value"] = {
            "decision_making": request.form.get("decision_making"),
            "monetization": request.form.get("monetization"),
            "time_savings": request.form.get("time_savings"),
            "reporting": request.form.get("reporting"),
            "processes": request.form.get("processes"),
            "collaboration": request.form.get("collaboration"),
            "documentation_audits": request.form.get("documentation_audits"),
        }

        data_store["product_owner_main"] = {
            "product_owner_name": request.form.get("product_owner_name"),
            "product_owner_zid": request.form.get("product_owner_zid"),
            "product_owner_email": request.form.get("product_owner_email"),
            "valid_from_date": request.form.get("valid_from_date"),
            "valid_to_date": request.form.get("valid_to_date"),
        }

        # Redirect to Step 2
        return redirect(url_for("step2"))

    return render_template("step1.html", data_store=data_store)


@app.route("/step2", methods=["GET", "POST"])
def step2():
    if request.method == "POST":
        action = request.form.get("action")

        # Handle skip action
        if action == "skip":
            data_store["product_owners"] = []  # Clear product owners data
            return redirect(url_for("step3"))

        # Initialize the product owners list
        product_owners = []
        for key in request.form.keys():
            if key.startswith("name-Subform-"):
                suffix = key.split("name-Subform-")[1]
                zid = request.form.get(f"zid-Subform-{suffix}")
                email = request.form.get(f"email-Subform-{suffix}")

                # Server-side validations
                if not zid or not re.match(r"^[a-zA-Z0-9]{6}$", zid):
                    return f"Invalid ZID: {zid}. Must be 6 alphanumeric characters.", 400
                if not is_valid_email(email):
                    return f"Invalid email: {email}. Must end with @xyz.com.", 400

                product_owners.append({
                    "name": request.form.get(f"name-Subform-{suffix}"),
                    "zid": zid,
                    "email": email,
                    "type": request.form.get(f"type-Subform-{suffix}", "Member"),
                    "valid_from": request.form.get(f"valid_from-Subform-{suffix}", datetime.today().strftime("%Y-%m-%d")),
                    "valid_to": request.form.get(f"valid_to-Subform-{suffix}", "9999-12-31"),
                })

        # Save to the data store
        data_store["product_owners"] = product_owners

        # Redirect based on action
        if action == "back_to_step1":
            return redirect(url_for("step1"))
        elif action == "next_to_step3":
            return redirect(url_for("step3"))

    # On GET, load existing data if any
    product_owners = data_store.get("product_owners", [])
    return render_template("step2.html", product_owners=product_owners)


@app.route("/step3", methods=["GET", "POST"])
def step3():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "skip":
            data_store["business_owners"] = []
            return redirect(url_for("step4"))


        # Initialize the list for storing business owners
        business_owners = []

        # Collect business owner data from the form
        for key in request.form.keys():
            if key.startswith("name-Subform-"):
                suffix = key.split("name-Subform-")[1]
                zid = request.form.get(f"zid-Subform-{suffix}")
                email = request.form.get(f"email-Subform-{suffix}")

                # Server-side validations
                if not zid or not re.match(r"^[a-zA-Z0-9]{6}$", zid):
                    return f"Invalid ZID: {zid}. Must be 6 alphanumeric characters.", 400
                if not is_valid_email(email):
                    return f"Invalid email: {email}. Must end with @xyz.com.", 400

                # Append valid data to the list
                business_owners.append({
                    "name": request.form.get(f"name-Subform-{suffix}"),
                    "zid": zid,
                    "email": email,
                    "type": request.form.get(f"type-Subform-{suffix}", "Owner"),
                    "valid_from": request.form.get(f"valid_from-Subform-{suffix}", datetime.today().strftime("%Y-%m-%d")),
                    "valid_to": request.form.get(f"valid_to-Subform-{suffix}", "9999-12-31"),
                })

        # Save data to the data_store
        data_store["business_owners"] = business_owners

        # Redirect based on the action
        if action == "back_to_step2":
            return redirect(url_for("step2"))
        elif action == "next_to_step4":
            return redirect(url_for("step4"))

    # On GET request, load existing business owner data if available
    business_owners = data_store.get("business_owners", [])
    return render_template("step3.html", business_owners=business_owners)


@app.route("/step4", methods=["GET", "POST"])
def step4():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "skip":
            data_store["snowflake_data_sources"] = []
            return redirect(url_for("step5"))

        snowflake_data_sources = []
        for key in request.form.keys():
            if key.startswith("database-Subform-"):
                suffix = key.split("database-Subform-")[1]

                # Collect data without additional validation
                snowflake_data_sources.append({
                    "database_name": request.form.get(f"database-Subform-{suffix}"),
                    "schema_name": request.form.get(f"schema-Subform-{suffix}"),
                    "table_name": request.form.get(f"table-Subform-{suffix}"),
                    "data_type": request.form.get(f"data_type-Subform-{suffix}", "Source"),
                    "valid_from": request.form.get(f"valid_from-Subform-{suffix}", datetime.today().strftime("%Y-%m-%d")),
                    "valid_to": request.form.get(f"valid_to-Subform-{suffix}", "9999-12-31"),
                })

        data_store["snowflake_data_sources"] = snowflake_data_sources
        # Redirect based on the action
        if action == "back_to_step3":
            return redirect(url_for("step3"))
        elif action == "next_to_step5":
            return redirect(url_for("step5"))

    snowflake_data_sources = data_store.get("snowflake_data_sources", [])
    # Populate the form with existing data if available
    return render_template("step4.html", snowflake_data_sources=snowflake_data_sources)


@app.route("/step5", methods=["GET", "POST"])
def step5():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "skip":
            data_store["other_data_sources"] = []
            return redirect(url_for("step6"))

        other_data_sources = []
        for key in request.form.keys():
            if key.startswith("dataset-Subform-"):
                suffix = key.split("dataset-Subform-")[1]

                # Collect data without additional validation
                other_data_sources.append({
                    "dataset_name": request.form.get(f"dataset-Subform-{suffix}"),
                    "dataset_description": request.form.get(f"description-Subform-{suffix}"),
                    "data_type": request.form.get(f"data_type-Subform-{suffix}"),
                    "dataset_type": request.form.get(f"dataset_type-Subform-{suffix}", "Source"),
                    "valid_from": request.form.get(f"valid_from-Subform-{suffix}", datetime.today().strftime("%Y-%m-%d")),
                    "valid_to": request.form.get(f"valid_to-Subform-{suffix}", "9999-12-31"),
                })

        data_store["other_data_sources"] = other_data_sources
        
        # Redirect based on the action
        if action == "back_to_step4":
            return redirect(url_for("step4"))
        elif action == "next_to_step6":
            return redirect(url_for("step6"))

    # On GET request, load existing business owner data if available
    other_data_sources = data_store.get("other_data_sources", [])
    return render_template("step5.html", other_data_sources=other_data_sources)


@app.route("/step6", methods=["GET", "POST"])
def step6():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "skip":
            data_store["platforms"] = []
            return redirect(url_for("review_page"))


        platforms = []
        for key in request.form.keys():
            if key.startswith("platform_name-Subform-"):
                suffix = key.split("platform_name-Subform-")[1]

                platforms.append({
                    "platform_name": request.form.get(f"platform_name-Subform-{suffix}"),
                    "platform_description": request.form.get(f"platform_description-Subform-{suffix}"),
                    "valid_from": request.form.get(f"valid_from-Subform-{suffix}", datetime.today().strftime("%Y-%m-%d")),
                    "valid_to": request.form.get(f"valid_to-Subform-{suffix}", "9999-12-31"),
                })

        data_store["platforms"] = platforms

        if action == "back_to_step5":
            return redirect(url_for("step5"))
        elif action == "next_to_review":
            return redirect(url_for("review_page"))
    platforms = data_store.get("platforms", [])
    # Populate the form with existing data if available
    return render_template("step6.html", platforms=platforms)


@app.route("/review", methods=["GET", "POST"])
def review_page():
    return render_template("review.html", data_store=data_store)


@app.route("/submit_to_snowflake", methods=["POST"])
def submit_to_snowflake():
    statuses = {}
    try:
        # Example logic for saving to Snowflake
        statuses["step1"] = save_to_snowflake("step1_table", data_store.get("product_info", {}))
        statuses["step2"] = save_to_snowflake("step2_table", data_store.get("product_owners", []))
        statuses["step3"] = save_to_snowflake("step3_table", data_store.get("business_owners", []))
        statuses["step4"] = save_to_snowflake("step4_table", data_store.get("snowflake_data_sources", []))
        statuses["step5"] = save_to_snowflake("step5_table", data_store.get("other_data_sources", []))
        statuses["step6"] = save_to_snowflake("step6_table", data_store.get("platforms", []))
    except Exception as e:
        statuses = {step: "Failed" for step in ["step1", "step2", "step3", "step4", "step5", "step6"]}
        statuses["error"] = str(e)

    return render_template("thank_you.html", statuses=statuses)


@app.route("/restart_submission", methods=["GET"])
def restart_submission():
    global data_store  # Clear or reset the data store
    data_store = {
        "product_info": {},
        "business_value": {},
        "product_owner_main": {},
        "product_owners": [],
        "business_owners": [],
        "snowflake_data_sources": [],
        "other_data_sources": [],
        "platforms": [],
    }
    return redirect(url_for("step1"))


def save_to_snowflake(table_name, data):
    # Placeholder logic for inserting data into Snowflake
    try:
        # Simulate a save operation
        print(f"Saving data to {table_name}: {data}")
        return "Success"
    except Exception as e:
        print(f"Error saving to {table_name}: {e}")
        return "Failed"


if __name__ == "__main__":
    app.run(debug=True)
