/*************************************
@@File: Job Stock  Template Custom Js

All custom js files contents are below
**************************************
* 00. Loader
* 01. Company Brand Carousel
* 02. Client Story testimonial
* 03. Bootstrap wysihtml5 editor
* 04 Grid Slider
* 05 Grid Slider 2
* 06. Tab Js
* 07. Add field Script
* 08 Add Field
* 09 Background Image
* 10 City Select
* 11 Styles
**************************************/

function pasteStudentEducationValues(e){
    var button = e.target;
    var form = document.querySelector('#edit-student-education-form');
    form.university_name.value = button.dataset.university_name;
    form.locality.value = button.dataset.locality;
    form.degree_program.value = button.dataset.degree_program;
    form.description.value = button.dataset.description;
    form.start_year.value = button.dataset.start_year;
    form.finish_year.value = button.dataset.finish_year;
    form.pk.value = button.dataset.id;

    var study_cycles = document.querySelectorAll('option.student-education-study_cycle');
    study_cycles.forEach(function callback(obj, index, array){
        obj.removeAttribute('selected');
        if (obj.value == button.dataset.study_cycle) {
            obj.setAttribute('selected', 'selected');
        }
    });
};

function deleteStudentEducation(e){
    let button = e.target;
    student_education_id = button.dataset.id;
    $.ajax({
        url: '/api/student/education/'+ student_education_id +'/delete',
        type: 'get',
        success: function(data) {
            changeStudentEducation(data.student_education);
        },
        failure: function(data) { 
            console.log(data);
        }
    });
}

function changeStudentEducation(student_education, student_education_form){
    var studentEducationBlock = document.querySelector('#student_education_list');
    var editDisplayValue = studentEducationBlock.dataset.edit;
    var deleteDisplayValue = studentEducationBlock.dataset.delete;
    var updatedstudentEducationBlock = '';
    student_education.forEach(function callback(education, index, array){
        updatedstudentEducationBlock +=
        '<li><div class="trim-edu">\
            <h4 class="trim-edu-title">\
                '+ education.fields.university_name +'\
                <span class="title-est">'+ education.fields.start_year +' - '+ education.fields.finish_year +'</span>\
                <span class="title-est">('+ education.fields.locality +')</span>\
            </h4>\
            <p><strong>'+ education.fields.degree_program +'</strong></p>\
            <p>'+ education.fields.study_cycle +'</p>\
            <p>'+ education.fields.description +'</p>\
            <button type="button" class="btn btn-success edit-student-education-btn" data-toggle="modal"\
                data-target="#edit_student_education_modal" data-id="'+ education.pk +'"\
                data-university_name="'+ education.fields.university_name +'" data-start_year="'+ education.fields.start_year +'"\
                data-finish_year="'+ education.fields.finish_year +'" data-locality="'+ education.fields.locality +'"\
                data-degree_program="'+ education.fields.degree_program +'" data-study_cycle="'+ education.fields.study_cycle +'"\
                data-description="'+ education.fields.description +'">\
                '+ editDisplayValue +'\
            </button>\
            <button type="button" class="btn btn-default delete-student-education" data-id="'+ education.pk +'"">'+ deleteDisplayValue +'</button>\
        </div></li>';
    });
    studentEducationBlock.innerHTML = updatedstudentEducationBlock;
    $('#create_student_education button[aria-label=Close]').click()
    var modals = $('.modal-edit-student-education button[aria-label=Close]');
    modals.click();
    
    let buttonsDeleted = document.querySelectorAll('button.delete-student-education');
    buttonsDeleted.forEach(button => button.addEventListener('click', deleteStudentEducation));

    let buttonsEdited = document.querySelectorAll('button.edit-student-education-btn');
    buttonsEdited.forEach(button => button.addEventListener('click', pasteStudentEducationValues));
}


(function($){
"use strict";

	//Loader
	$(window).on('load', function() {
		$(".Loader").fadeOut("slow");;
	});
	 
	 /*---Company Brand Carousel --*/
	 $("#company-brands").owlCarousel({
		items:5,
		itemsDesktop:[1199,5],
		itemsDesktopSmall:[979,4],
		itemsTablet:[768,3],
		itemsMobile: [600, 2],
		loop:true,
		pagination: false,
		navigation:false,
		navigationText:["",""],
		autoPlay:true
	});
	
	/*--- Client Story testimonial --*/
	$("#client-testimonial-slider").owlCarousel({
		items:3,
		itemsDesktop:[1199,3],
		itemsDesktopSmall:[979,2],
		itemsTablet:[768,1],
		pagination: false,
		navigation:false,
		navigationText:["",""],
		autoPlay:true
	});
	
	/*---Bootstrap wysihtml5 editor --*/	
	$('.textarea').wysihtml5();
	
	/*------ Grid Slider ----*/
	$('.grid-slide').slick({
	  slidesToShow:3,
	  arrows:false,
	  autoplay:true,
	  infinite: true,
	  responsive: [
		{
		  breakpoint: 768,
		  settings: {
			arrows:false,
			centerMode: true,
			slidesToShow:2
		  }
		},
		{
		  breakpoint: 480,
		  settings: {
			arrows: false,
			centerPadding: '0px',
			slidesToShow: 1
		  }
		}
	  ]
	});
	
	/*------ Grid Slider ----*/
	$('.grid-slide-2').slick({
	  slidesToShow:2,
	  arrows:false,
	  autoplay:true,
	  infinite: true,
	  responsive: [
		{
		  breakpoint: 768,
		  settings: {
			arrows:false,
			centerMode: true,
			slidesToShow:1
		  }
		},
		{
		  breakpoint: 480,
		  settings: {
			arrows: false,
			centerPadding: '0px',
			slidesToShow: 1
		  }
		}
	  ]
	});
	
	/*---Tab Js --*/
	$("#simple-design-tab a").on('click', function(e){
		e.preventDefault();
		$(this).tab('show');
	});
	
	/*-----Add field Script------*/
	$('.extra-field-box').each(function() {
    var $wrapp = $('.multi-box', this);
    $(".add-field", $(this)).on('click', function() {
        $('.dublicat-box:first-child', $wrapp).clone(true).appendTo($wrapp).find('input').val('').focus();
    });
    $('.dublicat-box .remove-field', $wrapp).on('click', function() {
        if ($('.dublicat-box', $wrapp).length > 1)
            $(this).parent('.dublicat-box').remove();
		});
	});
	
	//   Background image ------------------
		var a = $(".bg");
		a.each(function (a) {
			if ($(this).attr("data-bg")) $(this).css("background-image", "url(" + $(this).data("bg") + ")");
		});
		
		$('.slideshow-container').slick({
        slidesToShow: 1,
        autoplay: true,
        autoplaySpeed:2000,
        arrows: false,
        fade: true,
        cssEase: 'ease-in',
        infinite: true,
        speed:2000
    });
	
	// City Select
	$('#choose-city').select2();
	
	// Category Select
	$('#choose-category').select2();

    $('#j-category').select2();

    $('#select-company').select2();
	
	// Category Select
	
	// --------- Job List --------
	var options = {
		url: "./assets/js/resources/joblist.json",

		getValue: "name",

		list: {
			match: {
				enabled: true
			}
		}
	};
	
	// --------- Companies --------
	var options = {
		url: "./assets/js/resources/companies.json",

		getValue: "name",

		list: {
			match: {
				enabled: true
			}
		}
	};

	$("#companies").easyAutocomplete(options);
	
	// --------- Location --------
	var options = {
		url: "./assets/js/resources/location.json",

		getValue: "name",

		list: {
			match: {
				enabled: true
			}
		}
	};

	$("#location").easyAutocomplete(options);
		
	// Styles ------------------
    function csselem() {
        $(".slideshow-container .slideshow-item").css({
            height: $(".slideshow-container").outerHeight(true)
        });
        $(".slider-container .slider-item").css({
            height: $(".slider-container").outerHeight(true)
        });
    }
    csselem();
    $('#user_birthdate').dateDropper({});
    $('#internship_applications_deadline').dateDropper({});
    $('#internship_start_date').dateDropper({});
    $('#internship_end_date').dateDropper({});

    $('#add_student_education').on('submit', function (e) {
        e.preventDefault();
        var formData = e.target.elements;
        var postData = {
            university_name: formData['university_name'].value,
            locality: formData['locality'].value,
            degree_program: formData['degree_program'].value,
            study_cycle: formData['study_cycle'].value,
            description: formData['description'].value,
            start_year: formData['start_year'].value,
            finish_year: formData['finish_year'].value
        };
        $.ajax({
            url: '/api/student/education/create',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentEducation(data.student_education);
                e.target.reset();
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    });

      // Browser supports HTML5 multiple file?
      var multipleSupport = typeof $('<input/>')[0].multiple !== 'undefined',
          isIE = /msie/i.test( navigator.userAgent );

      $.fn.customFile = function(params) {

        return this.each(function(params) {
          var value = $(this).data('value'),
              selected = $(this).data('selected'),
              label = $(this).data('label'),
              standart = $(this).data('standart');

          if (standart){
            standart = standart;
          }
          else {
            standart = 'Select a File'
          }


          if (value) {
            var $input = $('<a href="'+ value +'" download><input type="text" class="file-upload-input" value="'+ label +'"/></a>')
          }
          else if (selected) {
            var $input = $('<input type="text" class="file-upload-input" value="'+ selected +'"/>')
          }
          else {
            var $input = $('<input type="text" class="file-upload-input" value="NOT ATTACHED"/>')
          }
          var $file = $(this).addClass('custom-file-upload-hidden'), // the original file input
              $wrap = $('<div class="file-upload-wrapper">'),
              // Button that will be used in non-IE browsers
              $button = $('<button type="button" class="file-upload-button">'+ standart +'</button>'),
              // Hack for IE
              $label = $('<label class="file-upload-button" for="'+ $file[0].id +'">'+ standart +'</label>');



          // Hide by shifting to the left so we
          // can still trigger events
          $file.css({
            position: 'absolute',
            left: '-9999px'
          });

          $wrap.insertAfter( $file )
            .append( $file, $input, ( isIE ? $label : $button ) );

          // Prevent focus
          $file.attr('tabIndex', -1);
          $button.attr('tabIndex', -1);

          $button.click(function () {
            $file.focus().click(); // Open dialog
          });

          $file.change(function() {

            var files = [], fileArr, filename;

            // If multiple is supported then extract
            // all filenames from the file array
            if ( multipleSupport ) {
              fileArr = $file[0].files;
              for ( var i = 0, len = fileArr.length; i < len; i++ ) {
                files.push( fileArr[i].name );
              }
              filename = files.join(', ');

            // If not supported then just take the value
            // and remove the path to just show the filename
            } else {
              filename = $file.val().split('\\').pop();
            }

            $input.val( filename ) // Set the value
              .attr('title', filename) // Show filename in title tootlip
              .focus(); // Regain focus

          });

          $input.on({
            blur: function() { $file.trigger('blur'); },
            keydown: function( e ) {
              if ( e.which === 13 ) { // Enter
                if ( !isIE ) { $file.trigger('click'); }
              } else if ( e.which === 8 || e.which === 46 ) { // Backspace & Del
                // On some browsers the value is read-only
                // with this trick we remove the old input and add
                // a clean clone with all the original events attached
                $file.replaceWith( $file = $file.clone( true ) );
                $file.trigger('change');
                $input.val('');
              } else if ( e.which === 9 ){ // TAB
                return;
              } else { // All other keys
                return false;
              }
            }
          });

        });

      };

      // Old browser fallback
      if ( !multipleSupport ) {
        $( document ).on('change', 'input.customfile', function() {

          var $this = $(this),
              // Create a unique ID so we
              // can attach the label to the input
              uniqId = 'customfile_'+ (new Date()).getTime(),
              $wrap = $this.parent(),

              // Filter empty input
              $inputs = $wrap.siblings().find('.file-upload-input')
                .filter(function(){ return !this.value }),

              $file = $('<input type="file" id="'+ uniqId +'" name="'+ $this.attr('name') +'"/>');

          // 1ms timeout so it runs after all other events
          // that modify the value have triggered
          setTimeout(function() {
            // Add a new input
            if ( $this.val() ) {
              // Check for empty fields to prevent
              // creating new inputs when changing files
              if ( !$inputs.length ) {
                $wrap.after( $file );
                $file.customFile();
              }
            // Remove and reorganize inputs
            } else {
              $inputs.parent().remove();
              // Move the input so it's always last on the list
              $wrap.appendTo( $wrap.parent() );
              $wrap.find('input').focus();
            }
          }, 1);

        });
      }
	})(jQuery);


document.addEventListener("DOMContentLoaded", function(){
    let StudentSoftSkillInput = document.querySelector('input[list="searched_student_soft_skills"]');
    let last_skills = [];
    let last_search = {};

    let ChangeStudentSoftSkills = async function(skills){
        if (JSON.stringify(skills) !== JSON.stringify(last_skills)) {
            let dataList = document.querySelector('#searched_student_soft_skills');
            updatedDatalistHTML = ''
            skills.forEach(skill => updatedDatalistHTML += '<option>' + skill.name)
            dataList.innerHTML = '';
            await new Promise(r => setTimeout(r, 200));
            dataList.innerHTML = updatedDatalistHTML;
            last_skills = skills;
        }
    }
    let onStudentSkillInput = function(e){
        let input = e.target,
            input_value = input.value;
        
        $.ajax({
            url: '/api/student/search-skills?name='+ input_value +'&skill_type=soft',
            type: 'get',
            success: function(data) {
                ChangeStudentSoftSkills(data.student_skills);
            },
            failure: function(data) { 
                console.log('StudentSoftSkillInput: Error...', data);
            }
        });
    }
    StudentSoftSkillInput.addEventListener('input', onStudentSkillInput);
});


document.addEventListener("DOMContentLoaded", function(){
    let StudentHardSkillInput = document.querySelector('input[list="searched_student_hard_skills"]');
    let last_skills = [];
    let last_search = {};

    let ChangeStudentHardSkills = async function(skills){
        if (JSON.stringify(skills) !== JSON.stringify(last_skills)) {
            let dataList = document.querySelector('#searched_student_hard_skills');
            updatedDatalistHTML = ''
            skills.forEach(skill => updatedDatalistHTML += '<option>' + skill.name)
            dataList.innerHTML = '';
            await new Promise(r => setTimeout(r, 200));
            dataList.innerHTML = updatedDatalistHTML;
            last_skills = skills;
        }
    }
    let onStudentSkillInput = function(e){
        let input = e.target,
            input_value = input.value;
        
        $.ajax({
            url: '/api/student/search-skills?name='+ input_value +'&skill_type=hard',
            type: 'get',
            success: function(data) {
                ChangeStudentHardSkills(data.student_skills);
            },
            failure: function(data) { 
                console.log('StudentHardSkillInput: Error...', data);
            }
        });
    }
    StudentHardSkillInput.addEventListener('input', onStudentSkillInput);
});


function ChangeSignUpType(signup_type) {
	document.getElementById("signup_type").value = signup_type;
    var signup_type_student = document.getElementById("signup_type_student");
    var signup_type_university = document.getElementById("signup_type_university");
    var signup_type_company = document.getElementById("signup_type_company");

   	signup_type_student.classList.remove('btn-success');
   	signup_type_university.classList.remove('btn-success');
   	signup_type_company.classList.remove('btn-success');

   	signup_type_student.classList.add('btn-default');
   	signup_type_university.classList.add('btn-default');
   	signup_type_company.classList.add('btn-default');

   	var input_name = document.getElementById("signup_name");
   	input_name.setAttribute('name', 'name');

   	if (signup_type == 'student') {
   		signup_type_student.classList.remove('btn-default');
   		signup_type_student.classList.add('btn-success');
   		input_name.setAttribute('name', 'full_name');
   	}
   	else if (signup_type == 'university') {
   		signup_type_university.classList.remove('btn-default');
   		signup_type_university.classList.add('btn-success');
   	}
   	else if (signup_type == 'company') {
   		signup_type_company.classList.remove('btn-default');
   		signup_type_company.classList.add('btn-success');
   	}
}

document.addEventListener("DOMContentLoaded", function(){
    function updateStudentEducation(e){
        e.preventDefault();
        let form = e.target;
        var formData = form.elements;
        var student_education_id = form['pk'].value;
        console.log(student_education_id);
        var postData = {
            university_name: formData['university_name'].value,
            locality: formData['locality'].value,
            degree_program: formData['degree_program'].value,
            study_cycle: formData['study_cycle'].value,
            description: formData['description'].value,
            start_year: formData['start_year'].value,
            finish_year: formData['finish_year'].value
        };
        $.ajax({
            url: '/api/student/education/'+ student_education_id +'/edit',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentEducation(data.student_education);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    };

    let formUpdated = document.querySelector('#edit-student-education-form');
    formUpdated.addEventListener('submit', updateStudentEducation);

    let buttonsDeleted = document.querySelectorAll('button.delete-student-education');
    buttonsDeleted.forEach(button => button.addEventListener('click', deleteStudentEducation));

    let buttonsEdited = document.querySelectorAll('button.edit-student-education-btn');
    buttonsEdited.forEach(button => button.addEventListener('click', pasteStudentEducationValues));
});


document.addEventListener("DOMContentLoaded", function(){
    function changeStudentWork(student_work) {
        console.log(student_work);
        var studentWorkBlock = document.querySelector('#student_work_list');
        var editDisplayValue = studentWorkBlock.dataset.edit;
        var deleteDisplayValue = studentWorkBlock.dataset.delete;
        var updatedStudentWorkBlock = '';
        student_work.forEach(function callback(obj, index, array){
            updatedStudentWorkBlock +=
            '<li><div class="trim-edu">\
                <h4 class="trim-edu-title">\
                    '+ obj.fields.company_name +'\
                    <span class="title-est">'+ obj.fields.start_year +' - '+ obj.fields.finish_year +'</span>\
                    <span class="title-est">('+ obj.fields.locality +')</span>\
                </h4>\
                <p><strong>'+ obj.fields.position_held +'</strong></p>\
                <p>'+ obj.fields.description +'</p>\
                <button type="button" class="btn btn-success edit-student-work-btn" data-toggle="modal"\
                    data-target="#edit_student_work_modal" data-id="'+ obj.pk +'"\
                    data-company_name="'+ obj.fields.company_name +'" data-start_year="'+ obj.fields.start_year +'"\
                    data-finish_year="'+ obj.fields.finish_year +'" data-locality="'+ obj.fields.locality +'"\
                    data-position_held="'+ obj.fields.position_held +'" data-description="'+ obj.fields.description +'">\
                    '+ editDisplayValue +'\
                </button>\
                <button type="button" class="btn btn-default delete-student-work" data-id="'+ obj.pk +'"">'+ deleteDisplayValue +'</button>\
            </div></li>';
        });
        studentWorkBlock.innerHTML = updatedStudentWorkBlock;
        $('#create_student_work button[aria-label=Close]').click()
        var modals = $('.modal-edit-student-work button[aria-label=Close]');
        modals.click();
        afterRequest();
    };

    function createStudentWork(e) {
        e.preventDefault();
        var formData = e.target.elements;
        var postData = {
            company_name: formData['company_name'].value,
            locality: formData['locality'].value,
            position_held: formData['position_held'].value,
            description: formData['description'].value,
            start_year: formData['start_year'].value,
            finish_year: formData['finish_year'].value
        };
        $.ajax({
            url: '/api/student/work/create',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentWork(data.student_work);
                e.target.reset();
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    };

    function updateStudentWork(e) {
        e.preventDefault();
        var formData = e.target.elements;
        student_work_id = e.target.elements.pk.value;
        var postData = {
            company_name: formData['company_name'].value,
            locality: formData['locality'].value,
            position_held: formData['position_held'].value,
            description: formData['description'].value,
            start_year: formData['start_year'].value,
            finish_year: formData['finish_year'].value
        };
        $.ajax({
            url: '/api/student/work/'+ student_work_id +'/edit',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentWork(data.student_work);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    };

    function pasteStudentWorkValues(e) {
        var button = e.target;
        var form = document.querySelector('#edit-student-work-form');
        form.company_name.value = button.dataset.company_name;
        form.locality.value = button.dataset.locality;
        form.position_held.value = button.dataset.position_held;
        form.description.value = button.dataset.description;
        form.start_year.value = button.dataset.start_year;
        form.finish_year.value = button.dataset.finish_year;
        form.pk.value = button.dataset.id;
    };

    function deleteStudentWork(e){
        let button = e.target;
        student_work_id = button.dataset.id;
        $.ajax({
            url: '/api/student/work/'+ student_work_id +'/delete',
            type: 'get',
            success: function(data) {
                changeStudentWork(data.student_work);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    }

    function afterRequest() {
        var buttonsDeleted = document.querySelectorAll('button.delete-student-work');
        buttonsDeleted.forEach(button => button.addEventListener('click', deleteStudentWork));

        var buttonsEdited = document.querySelectorAll('button.edit-student-work-btn');
        buttonsEdited.forEach(button => button.addEventListener('click', pasteStudentWorkValues));
    }

    let formCreated = document.querySelector('#add_student_work');
    formCreated.addEventListener('submit', createStudentWork);

    let formUpdated = document.querySelector('#edit-student-work-form');
    formUpdated.addEventListener('submit', updateStudentWork);

    let buttonsDeleted = document.querySelectorAll('button.delete-student-work');
    buttonsDeleted.forEach(button => button.addEventListener('click', deleteStudentWork));

    let buttonsEdited = document.querySelectorAll('button.edit-student-work-btn');
    buttonsEdited.forEach(button => button.addEventListener('click', pasteStudentWorkValues));
});


document.addEventListener("DOMContentLoaded", function(){
    function changeStudentPublication(student_publication) {
        console.log(student_publication);
        var studentPublicationBlock = document.querySelector('#student_publications_list');
        var editDisplayValue = studentPublicationBlock.dataset.edit;
        var deleteDisplayValue = studentPublicationBlock.dataset.delete;
        var updatedStudentPublicationBlock = '';
        student_publication.forEach(function callback(obj, index, array){
            updatedStudentPublicationBlock += '\
            <li>\
                <div class="trim-edu">\
                    <h4 class="trim-edu-title">'+ obj.fields.title +'\
                        <span class="title-est">'+ obj.fields.year +'</span>\
                    </h4>\
                    <strong>'+ obj.fields.author +'</strong>\
                    <p>'+ obj.fields.publisher +'</p>\
                    <button type="button" class="btn btn-success edit-student-publication-btn" data-toggle="modal"\
                        data-target="#edit_student_publication_modal" data-id="'+ obj.pk +'"\
                        data-title="'+ obj.fields.title +'" data-year="'+ obj.fields.year +'"\
                        data-author="'+ obj.fields.author +'" data-publisher="'+ obj.fields.publisher +'">\
                        '+ editDisplayValue +'\
                    </button>\
                    <button type="button" class="btn btn-default delete-student-publication"\
                    data-id="'+ obj.pk +'">'+ deleteDisplayValue +'</button>\
                </div>\
            </li>'
        });
        studentPublicationBlock.innerHTML = updatedStudentPublicationBlock;
        $('#create_student_publication button[aria-label=Close]').click();
        $('#edit_student_publication_modal button[aria-label=Close]').click();
        afterRequest();
    }

    function createStudentPublication(e) {
        e.preventDefault();
        var form = e.target;
        var formData = form.elements;
        var postData = {
            title: formData['title'].value,
            year: formData['year'].value,
            author: formData['author'].value,
            publisher: formData['publisher'].value
        };
        $.ajax({
            url: '/api/student/publication/create',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentPublication(data.student_publication);
                e.target.reset();
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    };

    function updateStudentPublication(e) {
        e.preventDefault();
        var formData = e.target.elements;
        console.log(e.target)
        var student_publication_id = e.target.elements.pk.value;
        var postData = {
            title: formData['title'].value,
            year: formData['year'].value,
            author: formData['author'].value,
            publisher: formData['publisher'].value
        };
        $.ajax({
            url: '/api/student/publication/'+ student_publication_id +'/edit',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentPublication(data.student_publication);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    };

    function deleteStudentPublication(e) {
        let button = e.target;
        student_publication_id = button.dataset.id;
        $.ajax({
            url: '/api/student/publication/'+ student_publication_id +'/delete',
            type: 'get',
            success: function(data) {
                changeStudentPublication(data.student_publication);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    };

    function pasteStudentPublicationValues(e) {
        var button = e.target;
        var form = document.querySelector('#edit-student-publication-form');
        form.title.value = button.dataset.title;
        form.year.value = button.dataset.year;
        form.author.value = button.dataset.author;
        form.publisher.value = button.dataset.publisher;
        form.pk.value = button.dataset.id;
    };

    function afterRequest() {
        let buttonsDeleted = document.querySelectorAll('button.delete-student-publication');
        buttonsDeleted.forEach(button => button.addEventListener('click', deleteStudentPublication));

        let buttonsEdited = document.querySelectorAll('button.edit-student-publication-btn');
        buttonsEdited.forEach(button => button.addEventListener('click', pasteStudentPublicationValues));
    }

    let formCreated = document.querySelector('#add_student_publication');
    formCreated.addEventListener('submit', createStudentPublication);

    let formUpdated = document.querySelector('#edit-student-publication-form');
    formUpdated.addEventListener('submit', updateStudentPublication);

    let buttonsDeleted = document.querySelectorAll('button.delete-student-publication');
    buttonsDeleted.forEach(button => button.addEventListener('click', deleteStudentPublication));

    let buttonsEdited = document.querySelectorAll('button.edit-student-publication-btn');
    buttonsEdited.forEach(button => button.addEventListener('click', pasteStudentPublicationValues));
});


document.addEventListener("DOMContentLoaded", function(){
    function afterRequest() {
        let buttonsRemove = document.querySelectorAll('.remove-student-soft-skill');
        buttonsRemove.forEach(button => button.addEventListener('click', removeSoftSkill));
    }
    function changeStudentSoftSkills(student_skills){
        var blockSoftSkills = document.querySelector('#soft-skills-list');
        var updatedHTML = '';
        student_skills.forEach(function callback(obj, index, array){
            updatedHTML += '<li class="skill-name">'+ obj.fields.name +'<button type="button" class="delete remove-student-soft-skill" data-id="'+ obj.pk +'">x</button></li>'
        });
        blockSoftSkills.innerHTML = updatedHTML;
        afterRequest();
    };

    function addSoftSkill(e){
        var input = document.querySelector('#student_soft_skill');
        var postData = {
            'name': input.value,
            'skill_type': 'soft'
        };
        $.ajax({
            url: '/api/student/skill/add',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentSoftSkills(data.student_skills);
                input.value = '';
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    };

    function removeSoftSkill(e){
        $.ajax({
            url: '/api/student/skill/'+ e.target.dataset.id +'/remove?skill_type=soft',
            type: 'get',
            success: function(data) {
                changeStudentSoftSkills(data.student_skills);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    }

    let buttonAdd = document.querySelector('#add_student_soft_skill_btn');
    buttonAdd.addEventListener('click', addSoftSkill);

    let buttonsRemove = document.querySelectorAll('.remove-student-soft-skill');
    buttonsRemove.forEach(button => button.addEventListener('click', removeSoftSkill));
});


document.addEventListener("DOMContentLoaded", function(){
    function afterRequest() {
        let buttonsRemove = document.querySelectorAll('.remove-student-hard-skill');
        buttonsRemove.forEach(button => button.addEventListener('click', removeHardSkill));
    }
    function changeStudentHardSkills(student_skills){
        var blockSoftSkills = document.querySelector('#hard-skills-list');
        var updatedHTML = '';
        student_skills.forEach(function callback(obj, index, array){
            updatedHTML += '<li class="skill-name">'+ obj.fields.name +'<button type="button" class="delete remove-student-hard-skill" data-id="'+ obj.pk +'">x</button></li>'
        });
        blockSoftSkills.innerHTML = updatedHTML;
        afterRequest();
    };

    function addHardSkill(e){
        var input = document.querySelector('#student_hard_skill');
        var postData = {
            'name': input.value,
            'skill_type': 'hard'
        };
        $.ajax({
            url: '/api/student/skill/add',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentHardSkills(data.student_skills);
                input.value = '';
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    };

    function removeHardSkill(e){
        $.ajax({
            url: '/api/student/skill/'+ e.target.dataset.id +'/remove?skill_type=hard',
            type: 'get',
            success: function(data) {
                changeStudentHardSkills(data.student_skills);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    }

    let buttonAdd = document.querySelector('#add_student_hard_skill_btn');
    buttonAdd.addEventListener('click', addHardSkill);

    let buttonsRemove = document.querySelectorAll('.remove-student-hard-skill');
    buttonsRemove.forEach(button => button.addEventListener('click', removeHardSkill));
});


document.addEventListener("DOMContentLoaded", function(){
    function afterRequest() {
        let buttonsRemove = document.querySelectorAll('.remove-student-language');
        buttonsRemove.forEach(button => button.addEventListener('click', removeStudentLanguage));
    }
    function changeStudentLanguages(student_languages){
        var blockLanguages = document.querySelector('#student-languages-list');
        var updatedHTML = '';
        student_languages.forEach(function callback(obj, index, array){
            updatedHTML += '\
                <li class="skill-name">\
                    '+ obj.fields.name +'\
                    <button type="button" class="delete remove-student-language"\
                        data-id="'+ obj.pk +'" class="delete">x</button>\
                </li>'
        });
        blockLanguages.innerHTML = updatedHTML;
        afterRequest();
    }
    function addStudentLanguage(e){
        var selection = document.querySelector('#student-language');
        var postData = {
            'pk': selection.value
        };
        $.ajax({
            url: '/api/student/language/add',
            type: 'post',
            data: postData,
            success: function(data) {
                changeStudentLanguages(data.student_languages);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    }
    function removeStudentLanguage(e){
        $.ajax({
            url: '/api/student/language/'+ e.target.dataset.id +'/remove',
            type: 'get',
            success: function(data) {
                changeStudentLanguages(data.student_languages);
            },
            failure: function(data) { 
                console.log(data);
            }
        });
    }

    let buttonAdd = document.querySelector('#add-student-language-btn');
    buttonAdd.addEventListener('click', addStudentLanguage);

    let buttonsRemove = document.querySelectorAll('.remove-student-language');
    buttonsRemove.forEach(button => button.addEventListener('click', removeStudentLanguage));
});

document.addEventListener("DOMContentLoaded", function(){
    function readURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            $('#student-photo').attr('src', e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]); // convert to base64 string
      }
    }
    let input = document.querySelector('#student-photo-input');
    input.addEventListener('change', function(e){
        readURL(e.target);
    });
});

document.addEventListener("DOMContentLoaded", function(){
    function readURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            $('#logo-photo').attr('src', e.target.result);
        }
        
        reader.readAsDataURL(input.files[0]); // convert to base64 string
      }
    }
    let input = document.querySelector('#logo-photo-input');
    console.log('??')
    input.addEventListener('change', function(e){
        console.log('YES');
        readURL(e.target);
    });
});