
import pandas as pd
from django.http import HttpResponse,JsonResponse
from django.http import Http404
import numpy as np
from django.shortcuts import render
from openpyxl import Workbook
import numpy as np
from .models import RoomDetails,UploadedCSV
from django.shortcuts import get_object_or_404, redirect



def generate_seating_plan(request):
    if request.method == 'POST':
        roomno = request.POST.get('roomno')
       
        # Fetch room details from the database
        try:
            room = RoomDetails.objects.get(roomno=roomno)
        except RoomDetails.DoesNotExist:
            # Handle the case where RoomDetails does not exist
            return render(request, 'students_strength_exceeds.html')
        number_of_row_in_room = room.rows
        number_of_col_in_room = room.columns

        # Fetch student register numbers from the database
        register_data = UploadedCSV.objects.values_list('RegNo', flat=True).distinct()

        # Calculate the maximum number of students the room can accommodate
        max_students = number_of_row_in_room * number_of_col_in_room

        if len(register_data) > max_students:
            # Students strength exceeds room size, return a custom response
            return render(request, 'students_strength_exceeds.html')
        else:
            # Create a dictionary to group students by prefix
            students_by_prefix = {}
            for student in register_data:
                prefix = student[:8]
                if prefix not in students_by_prefix:
                    students_by_prefix[prefix] = []
                students_by_prefix[prefix].append(student)

            # Create a list to store the final seating plan
            seatingPlan = []

            # Generate sequential orders for each prefix
            for prefix, students in students_by_prefix.items():
                sequential_order = [f'{prefix}{i:02}' for i in range(1, len(students) + 1)]
                students_by_prefix[prefix] = sequential_order

            # Arrange students ensuring no same-prefix students are adjacent
            while any(students_by_prefix.values()):
                for prefix in students_by_prefix.keys():
                    if students_by_prefix[prefix]:
                        student = students_by_prefix[prefix].pop(0)
                        seatingPlan.append(student)

            x, y, z = 1, number_of_row_in_room, number_of_col_in_room

            # Fill any remaining seats with '0'
            seatingPlan += ['XX' for _ in range(number_of_row_in_room * number_of_col_in_room - len(seatingPlan))]

            arr = np.array(seatingPlan, dtype=str).reshape((x, y, z))

            # Convert seating plan data to a DataFrame
            df = pd.DataFrame(arr[0])

            # Create a header row with the room number
            header = pd.DataFrame([['ROOM NO', roomno]])

            # Combine the header with the seating plan data
            df = pd.concat([header, df])

            # Create an Excel response
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = f'attachment; filename="seating_plan_{roomno}.xlsx"'

            # Write DataFrame to Excel
            df.to_excel(response, index=False, header=False)
            
            return response
    else:
        room_details = RoomDetails.objects.all()
        student_count = UploadedCSV.objects.count()
        for room in room_details:
            room.strength = room.rows * room.columns
        return render(request, 'room_selection2.html', {'room_details': room_details,'student_count': student_count})
        


def generate_seating_plan2(request):
    if request.method == 'POST':
        roomno = request.POST.get('roomno')
        # Fetch room details from the database
        try:
            room = RoomDetails.objects.get(roomno=roomno)
        except RoomDetails.DoesNotExist:
            # Handle the case where RoomDetails does not exist
            return render(request, 'students_strength_exceeds.html')
        number_of_row_in_room = room.rows
        number_of_col_in_room = room.columns

        # Fetch student register numbers from the database
        register_data = UploadedCSV.objects.values_list('RegNo', flat=True).distinct()
        max_students = number_of_row_in_room * number_of_col_in_room
        if len(register_data) > max_students:
            # Students strength exceeds room size, return a custom response
            return render(request, 'students_strength_exceeds.html')
        # Create a dictionary to group students by prefix
        else:
            students_by_prefix = {}
        for student in register_data:
            prefix = student[:8]
            if prefix not in students_by_prefix:
                students_by_prefix[prefix] = []
            students_by_prefix[prefix].append(student)

        # Create a list to store the final seating plan
        seatingPlan = []

        # Generate sequential orders for each prefix
        for prefix, students in students_by_prefix.items():
            sequential_order = [f'{prefix}{i:02}' for i in range(1, len(students) + 1)]
            students_by_prefix[prefix] = sequential_order

        # Arrange students ensuring no same-prefix students are adjacent
        while any(students_by_prefix.values()):
            for prefix in students_by_prefix.keys():
                if students_by_prefix[prefix]:
                    student = students_by_prefix[prefix].pop(0)
                    seatingPlan.append(student)

        x, y, z = 1, number_of_row_in_room, number_of_col_in_room

        # Fill any remaining seats with '0'
        seatingPlan += ['XX' for _ in range(number_of_row_in_room * number_of_col_in_room - len(seatingPlan))]

        arr = np.array(seatingPlan, dtype=str).reshape((x, y, z))


        return render(request, 'seating_plan.html', {'roomno': roomno, 'seating_plan': arr})
    else:
        room_details = RoomDetails.objects.all()
        student_count = UploadedCSV.objects.count()
        for room in room_details:
            room.strength = room.rows * room.columns
        return render(request, 'room_selection2.html', {'room_details': room_details,'student_count': student_count})
    
def generate_seating_plan3(request):
    if request.method == 'POST':
        selected_rooms = request.POST.getlist('selected_rooms')
        seating_arrangements = {}  # Dictionary to store seating arrangements for each room

        total_students = list(UploadedCSV.objects.values_list('RegNo', flat=True).distinct())

        prefix_counts = {}  # Dictionary to store student counts by prefix

        for roomno in selected_rooms:
            room = RoomDetails.objects.get(roomno=roomno)
            number_of_row_in_room = room.rows
            number_of_col_in_room = room.columns
            max_students = number_of_row_in_room * number_of_col_in_room

            # Distribute students to rooms
            current_room_students = total_students[:max_students]
            total_students = total_students[max_students:]

            seatingPlan = []

            students_by_prefix = {}
            for student in current_room_students:
                prefix = student[:8]
                if prefix not in students_by_prefix:
                    students_by_prefix[prefix] = []
                students_by_prefix[prefix].append(student)

            sequential_order = []
            for prefix, students in students_by_prefix.items():
                sequential_order.extend([f'{prefix}{i:02}' for i in range(1, len(students) + 1)])

            while any(students_by_prefix.values()):
                for prefix in students_by_prefix.keys():
                    if students_by_prefix[prefix]:
                        student = students_by_prefix[prefix].pop(0)
                        seatingPlan.append(student)

            # Fill any remaining seats with 'XX'
            seatingPlan += ['XX' for _ in range(max_students - len(seatingPlan))]

            x, y, z = 1, number_of_row_in_room, number_of_col_in_room
            arr = np.array(seatingPlan, dtype=str).reshape((x, y, z))

            seating_arrangements[roomno] = arr

            # Calculate student counts by prefix
            room_counts = {}  # Dictionary to store prefix counts for each room

            for roomno in selected_rooms:
                if roomno in seating_arrangements:
                    room_counts[roomno] = {}  # Initialize a dictionary for each room
                    for row in seating_arrangements[roomno][0]:
                        for r in row:
                            prefix = r[:8]
                            if prefix in room_counts[roomno]:
                                room_counts[roomno][prefix] += 1
                            else:
                                room_counts[roomno][prefix] = 1

            # Now, room_counts is a dictionary where keys are room numbers (roomno) and values are dictionaries
            # representing prefix counts for each room.

            # To create a flat list of tuples (roomno, prefix, count) for each room, you can use a nested loop:
            prefix_counts = []

            for roomno, prefix_count in room_counts.items():
                for prefix, count in prefix_count.items():
                    prefix_counts.append((roomno, prefix, count))
        return render(request, 'seating_plan2.html', {'seating_arrangements': seating_arrangements, 'prefix_counts': prefix_counts})
    else:
        room_list = RoomDetails.objects.all()
        student_count = UploadedCSV.objects.count()
        for room in room_list:
            room.strength = room.rows * room.columns
        return render(request, 'room_selection3.html', {'room_list': room_list,'student_count': student_count})

def generate_seating_plan4(request):
    if request.method == 'POST':
        selected_rooms = request.POST.getlist('selected_rooms')
        seating_arrangements = {}  # Dictionary to store seating arrangements for each room

        total_students = list(UploadedCSV.objects.values_list('RegNo', flat=True).distinct())

        for roomno in selected_rooms:
            room = RoomDetails.objects.get(roomno=roomno)
            number_of_row_in_room = room.rows
            number_of_col_in_room = room.columns
            max_students = number_of_row_in_room * number_of_col_in_room

            # Distribute students to rooms
            current_room_students = total_students[:max_students]
            total_students = total_students[max_students:]

            seatingPlan = []

            students_by_prefix = {}
            for student in current_room_students:
                prefix = student[:8]
                if prefix not in students_by_prefix:
                    students_by_prefix[prefix] = []
                students_by_prefix[prefix].append(student)

            sequential_order = []
            for prefix, students in students_by_prefix.items():
                sequential_order.extend([f'{prefix}{i:02}' for i in range(1, len(students) + 1)])

            while any(students_by_prefix.values()):
                for prefix in students_by_prefix.keys():
                    if students_by_prefix[prefix]:
                        student = students_by_prefix[prefix].pop(0)
                        seatingPlan.append(student)

            # Fill any remaining seats with 'XX'
            seatingPlan += ['XX' for _ in range(max_students - len(seatingPlan))]

            x, y, z = 1, number_of_row_in_room, number_of_col_in_room
            arr = np.array(seatingPlan, dtype=str).reshape((x, y, z))

            # Convert the NumPy array to a list
            seating_plan_list = arr.tolist()

            seating_arrangements[roomno] = seating_plan_list

        # Create an Excel file and write data
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="seating_plan.xlsx"'

        wb = Workbook()
        for roomno, seating_plan in seating_arrangements.items():
            ws = wb.create_sheet(title=f'Room {roomno}')
            for i in range(len(seating_plan)):
                for j in range(len(seating_plan[i])):
                    ws.append(seating_plan[i][j])

        wb.save(response)

        return response
    else:
        room_list = RoomDetails.objects.all()
        student_count = UploadedCSV.objects.count()
        for room in room_list:
            room.strength = room.rows * room.columns
        return render(request, 'room_selection3.html', {'room_list': room_list,'student_count': student_count})