from flask import Flask, request, jsonify
from pymongo import MongoClient
import traceback
from bson.objectid import ObjectId, InvalidId

client = MongoClient(host='kind_gould', port=27017, username='root', password='pass', authSource="admin") 
db = client.todoapp 
todoList = db.todolist 
todoColection = todoList.todo

app = Flask(__name__)

@app.route("/")
def index():
    return "hello world"

@app.route("/todo", methods=["POST"])
##Thêm
def add_todo():
    try: 
        new_todo = request.json
        todoColection.insert_one(new_todo)
        return jsonify(message="Thêm việc phải làm thành công!!"), 201
    except Exception as error_message:
        print(traceback.format_exc())
        return jsonify(message="Lỗi!!",error=str(error_message)), 500
##Lấy tất cả việc phải làm
@app.route("/todo",methods=["GET"])
def get_all_todo():
    try:
        all_todos = list(todoColection.find())
        for todo in all_todos:
            todo["_id"] = str(todo["_id"])
        return jsonify(all_todos),200
    except Exception as error_message:
        print(traceback.format_exc())
        return jsonify(message="Lỗi!!",error=str(error_message)), 500
##Cập nhật
@app.route("/todo/<todo_id>",methods=["PUT"])
def update_todo(todo_id):
    try:
        update_data = request.json
        try: 
            object_id = ObjectId(todo_id)
        except InvalidId:
            return jsonify(message="ID không hợp lệ!!"), 400
        result = todoColection.update_one({"_id": object_id}, {"$set": update_data})
        if result.modified_count > 0:
            return jsonify(message="Cập nhật thành công!!"), 200
        else: 
            return jsonify(message="Không tìm thấy!!"), 404
    except Exception as error_message:
        print(traceback.format_exc())
        return jsonify(message="Lỗi!!",error=str(error_message)), 500
##Xóa
@app.route("/todo/<todo_id>",methods=["DELETE"])
def delete_todo(todo_id):
    try:
        try:
            object_id = ObjectId(todo_id)
        except InvalidId:
            return jsonify(message="ID không hợp lệ!!"), 400
        result = todoColection.delete_one({"_id": object_id})
        if result.deleted_count > 0:
            return jsonify(message="Xóa thành công!!"), 200
        else: 
            return jsonify(message="Không tìm thấy!!"), 404
    except Exception as error_message:
        print(traceback.format_exc())
        return jsonify(message="Lỗi!!",error=str(error_message)), 500

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)