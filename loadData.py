# -*- codeing = utf-8 -*-
# @Time : 2022/10/6 16:37
# @Author : 朱镕钊
# @File ： init_table.py
# @Software : PyCharm
import random

import pandas as pd


def not_come_student(List, a, b):
    not_come_num = random.randint(a, b)  # 在[a,b]范围内随机生成没来的人数
    not_come_List = random.sample(List, not_come_num)  # 取出没来的同学的学号
    return not_come_List


# 生成总出勤表
def create_table(n_courses, n_times, n_students):
    courses_record = []  # 总出勤表

    col = ["student_id", "course_id", "Attended"]  # 三列分别表示学号，课程号，出勤情况
    ids = list(range(n_students))  # 学号
    course_ids = list(range(n_courses))  # 课程号列表
    classes = list(range(n_times))  # 课时数20节

    # 一门课程的出勤
    for course_id in course_ids:
        course_record = []  # 本门课程出勤表
        # 经常没来
        always_not_come_students_ids = not_come_student(ids, 5, 8)  # 生成缺席了该课程80%的课的5-8位同学的ID
        always_not_come_times = int(n_times * 0.8)  # 没来的次数
        always_not_come_students_dict = {}  # 字典，记录每个经常缺勤的人没来的课时号
        for always_not_come_student_id in always_not_come_students_ids:
            not_Attended_classes = random.sample(classes, always_not_come_times)  # 生成经常不来的人没来的课时号
            always_not_come_students_dict[always_not_come_student_id] = not_Attended_classes  # 用字典记录下来：学号-缺勤课程号

        # 去除经常没来的学生的id号
        other_id = ids.copy()
        for always_not_come_student_id in always_not_come_students_ids:
            other_id.remove(always_not_come_student_id)

        # 为每个课时的考察表赋初值，总的有n_times个课时
        cnt = 0  # 课时序号
        for i in range(n_times):
            one_class_attend = pd.DataFrame(columns=col)  # 一个课时的出勤表
            one_class_attend["student_id"] = ids
            one_class_attend["course_id"] = course_id
            one_class_attend["Attended"] = 1  # 1表示来了，0表示没来

            # 为always没来的学生赋初值
            for always_not_come_student_id in always_not_come_students_ids:
                if cnt in always_not_come_students_dict[always_not_come_student_id]:
                    one_class_attend["Attended"].loc[always_not_come_student_id] = 0  # 没来则为0

            random.seed(None)
            seldom_not_come_students_id = not_come_student(other_id, 0, 3)
            for seldom_not_come_student_id in seldom_not_come_students_id:
                one_class_attend["Attended"].loc[seldom_not_come_student_id] = 0

            cnt += 1
            course_record.append(one_class_attend)  # 一门课程的出勤表

        courses_record.append(course_record)  # 一个学期所有课程的出勤表
    return courses_record


# 每门课程的出勤率表
def create_Course_average_Attendance(courses_record):
    Course_average_Attendance = []
    for course_record in courses_record:
        df1 = course_record[0][["student_id", "course_id"]].copy()
        df1['course_Attended_rate'] = 0
        sum1 = 0
        for one_class_attend in course_record:
            sum1 += 1
            df1['course_Attended_rate'] += one_class_attend["Attended"]  # 课程总出勤数
        df1['course_Attended_rate'] = df1['course_Attended_rate'] / sum1  # 课程的出勤率
        # df1['course_mean_Attendance_rate'] = df1.describe()["course_Attended_rate"]["mean"]
        # df1['course_std_Attendance_rate'] = df1.describe()["course_Attended_rate"]["std"]
        Course_average_Attendance.append(df1)
        # print(df1)
    return Course_average_Attendance


# 所有课程每个人的出勤率表
def create_total_average_Attendance(courses_record):
    df2 = courses_record[0][0][["student_id"]].copy()
    df2["total_Attended_rate"] = 0
    sum2 = 0
    for course_record in courses_record:
        for one_class_attend in course_record:
            sum2 += 1
            df2["total_Attended_rate"] += one_class_attend["Attended"]
    df2["total_Attended_rate"] = df2["total_Attended_rate"] / sum2  # 所有课程的出勤率
    # df2["total_mean_Attendance_rate"] = df2.describe()["total_Attended_rate"]["mean"]
    # df2["total_std_Attendance_rate"] = df2.describe()["total_Attended_rate"]["std"]
    return df2


# 把出勤表和学生个人的每门课程的出勤率以及总出勤率串联起来
def create_total_data(courses_record):
    data_list = []
    for i in range(len(courses_record)):
        data_ll = []
        for one_class_attend in courses_record[i]:
            data = one_class_attend.copy()
            data.drop("course_id", axis=1)
            Course_average_Attendance = create_Course_average_Attendance(courses_record)
            total_average_Attendance = create_total_average_Attendance(courses_record)
            # 连接课程出勤率
            data[Course_average_Attendance[i].columns[2:]] = Course_average_Attendance[i].iloc[:, 2:]
            # 连接总出勤率
            data[total_average_Attendance.columns[1:]] = total_average_Attendance.iloc[:, 1:]
            data_ll.append(data)
            data_list.append(data)
        data_ll = pd.concat(data_ll)
        data_ll.to_csv("course_" + str(i) + ".csv", index=False, header=True)

    total_data = pd.concat(data_list)
    return total_data, data_list


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)
num_times = 20  # 课时数
num_courses = 5  # 课程数
num_students = 90  # 学生数

cs_record = create_table(num_courses, num_times, num_students)
total_data, datalist = create_total_data(cs_record)
total_data.to_csv('total_data.csv', index=False, header=True)  # 输出为表格
