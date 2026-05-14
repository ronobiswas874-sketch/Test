from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# --- Database Connection ---
# আপনার নতুন তৈরি করা MongoDB URI এখানে যোগ করা হয়েছে
MONGO_URI = "mongodb+srv://ratnadipbagchi1_db_user:GU7b3gJjzy1Cry4U@cluster0.tsnhpjj.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['UserDatabase']
collection = db['PhoneRecords']

@app.route('/api/lookup', methods=['GET'])
def lookup_number():
    # Get the number from the URL parameter: /api/lookup?number=12345
    number = request.args.get('number')

    if not number:
        return jsonify({
            "status": "error",
            "message": "Mobile number is required"
        }), 400

    try:
        # Search the real database
        record = collection.find_one({"MOBILE": number})

        if record:
            # Match your exact requested response format
            response = {
                "Name": record.get("NAME", "N/A"),
                "Father's Name": record.get("fname", "N/A"),
                "Address": record.get("ADDRESS", "N/A"),
                "Circle": record.get("circle", "N/A"),
                "Mobile": record.get("MOBILE", "N/A"),
                "Alternate": record.get("alt", "N/A"),
                "ID": record.get("id", "N/A"),
                "Email": record.get("email", "N/A"),
                "developer": "@XEORX_MOD"
            }
            return jsonify(response), 200
        else:
            return jsonify({
                "status": "error",
                "message": "No real record found for this number"
            }), 404

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Use 0.0.0.0 to make it accessible via your VPS/Hosting IP
    app.run(host='0.0.0.0', port=5000, debug=True)
