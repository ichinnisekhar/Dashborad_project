import streamlit as st 
from helper import login_status_check,role_check
import requests
 
login_status_check() 
role_check('trainer')     

st.title("Trainer Dashboard")

loggedin_trainer_name = st.session_state['name']
loggedin_trainer_email = st.session_state['email']
loggedin_trainer_role = st.session_state['role']
loggedin_trainer_id = st.session_state['id']

st.write('Name  : ',loggedin_trainer_name)
st.write("Email : ",loggedin_trainer_email)
st.write("Role  : ",loggedin_trainer_role)

st.divider()
st.write("Trainer Features")
c1,c2 = st.columns(2)

with c1:
    if st.button('AddCourse'):
        st.session_state['add_course_status'] = True
with c2:
    if st.button("View My Courses"):
        st.session_state["view_my_courses_status"]=True


if st.session_state.get("add_course_status",False):    
    st.title('Add course form')
    with st.form("addCourseForm"):
        course_name = st.text_input('course name')
        description = st.text_area('Course description')
        duration = st.text_input('course duration')

        cl1,cl2 = st.columns(2)
        with cl1:
            if st.form_submit_button('addCourse'):
                new_course = {'trainer_id':loggedin_trainer_id, 
                                "course_name":course_name, 
                                "description":description,
                                "duration":duration
                                }
                res = requests.post('http://127.0.0.1:8000/add_course',json = new_course)
                if res.status_code == 200:
                    res_obj = res.json()
                    st.write(res_obj)
                else:
                    st.write("Some Error Occured")


if st.session_state.get("view_my_courses_status",False):
    res = requests.post("http://127.0.0.1:8000/get_my_courses",params={'t_id':loggedin_trainer_id})
    if res.status_code == 200:
        res_obj = res.json()
        st.dataframe(res_obj['data'])
    else:
        st.write("Some error occured")
