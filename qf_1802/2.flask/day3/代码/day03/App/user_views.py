
import random

from flask import Blueprint, render_template, request, url_for, redirect

from App.models import db, Student, Grade

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'


@user_blueprint.route('/drop_db/')
def drop_db():
    db.drop_all()
    return '删除成功'


@user_blueprint.route('/stu_list/')
def stu_list():
    # 使用orm
    # stus = Student.query.all()

    # 使用sql
    sql = 'select * from student'
    stus = db.session.execute(sql)

    return render_template('students.html', stus=stus)


@user_blueprint.route('/create_stu/', methods=['GET', 'POST'])
def create_stu():
    if request.method == 'GET':
        return render_template('create_student.html')

    if request.method == 'POST':
        username = request.form.get('username')
        stu = Student()
        stu.s_name = username

        db.session.add(stu)
        db.session.commit()

        return '创建%s学生成功' % username


@user_blueprint.route('/create_stus/', methods=['GET'])
def create_stus():

    stu_list = []
    for i in range(10):
        # 第一种方式
        # stu = Student()
        # stu.s_name = '温婉%s' % random.randrange(1000)
        # stu.s_age = '%s' % random.randrange(20)

        # 第二种
        stu = Student('温婉%s' % random.randrange(1000),
                      '%s' % random.randrange(20)
                      )

        stu_list.append(stu)

    db.session.add_all(stu_list)
    db.session.commit()
    return '创建小姐姐成功'


@user_blueprint.route('/update_stu/', methods=['GET', 'POST'])
def update_stu():

    if request.method == 'GET':
        id = request.args.get('id')
        stu = Student.query.filter(Student.s_id == id).first()
        return render_template('stu_edit.html', stu=stu)

    if request.method == 'POST':
        s_id = request.form.get('s_id')
        s_name = request.form.get('username')
        s_age = request.form.get('age')

        stu = Student.query.filter_by(s_id=s_id).first()
        stu.s_name = s_name
        stu.s_age = s_age
        # 修改，add操作可有可没有
        db.session.add(stu)
        db.session.commit()

        return redirect(url_for('user.stu_list'))


@user_blueprint.route('/stu_in/', methods=['GET'])
def stu_in_ids():
    # 1.查询学生的id在3到9之间的学生信息
    stus = Student.query.filter(Student.s_id.in_([3, 4, 5, 6, 7, 8, 9]))
    # 2.查询学生年龄小于19岁的
    stus = Student.query.filter(Student.s_age.__le__(19))
    # 3.查询姓名以9结束的学生信息
    stus = Student.query.filter(Student.s_name.endswith('9'))
    # 4.查询学生id为5的学生信息
    stus = Student.query.filter(Student.s_id == 5).all()
    stus = Student.query.get(5)
    # 模糊搜索
    # select * from student where s_name like '温婉%'
    stus = Student.query.filter(Student.s_name.like('%温婉%'))

    # 获取前五个
    stus = Student.query.limit(5)
    stus = Student.query.order_by('s_id').offset(3).limit(5)

    # 跳过几个
    stus = Student.query.order_by('s_id').offset(3)

    return render_template('students.html', stus=stus)


@user_blueprint.route('/paginate/', methods=['GET'])
def stu_paginate():
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        page_num = 10
        paginate = Student.query.order_by('s_id').paginate(page, page_num)
        stus = paginate.items

        return render_template('stu_paginate.html', stus=stus, paginate=paginate)


@user_blueprint.route('/add_grades/', methods=['GET'])
def add_grades():
    if request.method == 'GET':
        grades = {
            'python': '人生苦短，我用python',
            'php': '我是拍片的',
            'java': '入门到放弃',
            'go': 'go~go~go~go~'
        }
        g_list = []
        for key in grades:
            g = Grade()
            g.g_name = key
            g.g_desc = grades[key]
            g_list.append(g)
        db.session.add_all(g_list)
        db.session.commit()
        return '创建班级成功'


@user_blueprint.route('/grade_all/')
def grade_all():
    grades = Grade.query.all()
    return render_template('grades.html', grades=grades)


@user_blueprint.route('/create_stu_by_grade/', methods=['GET', 'POST'])
def create_stu_by_grade():
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        return render_template('create_student.html', g_id=g_id)

    if request.method == 'POST':
        g_id = request.form.get('g_id')
        username = request.form.get('username')

        stu = Student()
        stu.s_name = username
        stu.grades = g_id

        db.session.add(stu)
        db.session.commit()

        return redirect(url_for('user.grade_all'))


@user_blueprint.route('/select_stu_by_grade/', methods=['GET'])
def select_stu_by_grade():
    if request.method == 'GET':

        g_id = request.args.get('g_id')
        g = Grade.query.get(g_id)
        stus = g.students
        return render_template('students.html', stus=stus)


