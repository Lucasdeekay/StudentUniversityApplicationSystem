$(function(){

    $("#submit-btn").hide();

    $("#toast").fadeIn(5000);
    $("#toast").fadeOut(5000);

    $('#filter-registered-form').submit(function(e) {
        e.preventDefault();
        const level = $('#level').val();
        const semester = $('#semester').val();
        checkRegisteredCourseAvailability(level, semester);
    });

    $('#filter-form').submit(function(e) {
        e.preventDefault();
        const level = $('#level').val();
        const semester = $('#semester').val();
        checkCourseAvailability(level, semester);
    });

    function checkRegisteredCourseAvailability(level, semester) {
      $.ajax({
        url: "{% url 'get_registered_courses' %}",
        type: "POST",
        data: {
            level: level,
            semester: semester,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function(response) {
          // Update the table rows with available courses
          updateCourseTable(response.available_courses);
        },
        error: function(error) {
          console.error("Error fetching available courses:", error);
          // Handle errors appropriately (e.g., display an error message)
        },
      });
    }

    function checkCourseAvailability(level, semester) {
      $.ajax({
        url: "{% url 'get_courses' %}",
        type: "POST",
        data: {
            level: level,
            semester: semester,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function(response) {
          // Update the table rows with available courses
          updateCourseTable(response.available_courses);
        },
        error: function(error) {
          console.error("Error fetching available courses:", error);
          // Handle errors appropriately (e.g., display an error message)
        },
      });
    }

    function updateCourseTable(availableCourses) {
      $('#course_table tbody').empty(); // Clear existing rows
      $('#submit-btn').show();

      availableCourses.forEach(function(course) {
        const tableRow = $('<tr></tr>');
        tableRow.append($('<td></td>').text(course.title));
        tableRow.append($('<td></td>').text(course.code));
        tableRow.append($('<td></td>').text(course.units + ' Units'));
        tableRow.append($('<td></td>').append($('<input type="checkbox" name="course_id">')));
        $('#course_table tbody').append(tableRow);
      });
    }

})