from flask import Flask, request, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__)

# --- Database Connection ---
# SSL Error ফিক্স করার জন্য certifi.where() ব্যবহার করা হয়েছে
MONGO_URI = "mongodb+srv://ratnadipbagchi1_db_user:GU7b3gJjzy1Cry4U@cluster0.tsnhpjj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client['UserDatabase']
    collection = db['PhoneRecords']
except Exception as e:
    print(f"Database Connection Error: {e}")

@app.route('/api/lookup', methods=['GET'])
def lookup_number():
    number = request.args.get('number')

    if not number:
        return jsonify({
            "status": "error",
            "message": "Mobile number is required"
        }), 400

    try:
        # Search the database
        record = collection.find_one({"MOBILE": number})

        if record:
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

# Vercel-এর জন্য app অবজেক্টটি এক্সপোর্ট করা হলো
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
