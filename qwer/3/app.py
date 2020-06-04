from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/reviews', methods=['POST'])
def write_review():

    # 클라이언트가 준 정보 가저오기

    name_receive = request.form['name_give']
    count_receive = request.form['count_give']
    address1_receive = request.form['address1_give']
    address2_receive = request.form['address2_give']
    address3_receive = request.form['address3_give']
    phone_receive = request.form['phone_give']
    
    # DB에 삽입할 doc 만들기

    doc = {
        'name' : name_receive,
        'count' : count_receive,
        'address1' : address1_receive,
        'address2' : address2_receive,
        'address3' : address3_receive,
        'phone' : phone_receive   
    }
    # orders에 doc 저장하기

    db.orders.insert_one(doc)

    # 성공 여부 & 성공 메시지 반환

    return jsonify({'result':'success', 'msg': '주문이 성공적으로 완료되었습니다.'})


@app.route('/reviews', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    orders = list(db.orders.find({},{'_id':0}))
    
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result':'success', 'all_orders': orders})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)