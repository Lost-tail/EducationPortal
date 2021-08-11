


SelectUniversityObj = document.getElementById("SelectUniversity");
SelectCompanyObj = document.getElementById("SelectCompany");

AddNewStaffUserButtonSelect1obj = document.getElementById("AddNewStaffUserButtonSelect1");
AddNewStaffUserButtonSelect2obj = document.getElementById("AddNewStaffUserButtonSelect2");
AddNewStaffUserButtonSelect3obj = document.getElementById("AddNewStaffUserButtonSelect3");



function AddNewStaffUserButtonClick1() {

    SelectUniversityObj.style="display:none;";
    SelectCompanyObj.style="display:none;";

    document.getElementById("staff_type").value = "SuperAdmin";
    
}

function AddNewStaffUserButtonClick2() {

    SelectUniversityObj.style="display:block;";
    SelectCompanyObj.style="display:none;";

    document.getElementById("staff_type").value = "University Representative";

}

function AddNewStaffUserButtonClick3() {

    SelectUniversityObj.style="display:none;";
    SelectCompanyObj.style="display:block;";

    document.getElementById("staff_type").value = "Company Representative";

}



document.getElementById("AddNewStaffUserButtonSelect1").focus();




$('.datepicker').datepicker({
    format: 'dd/mm/yyyy',
    startDate: '-3d'
});
