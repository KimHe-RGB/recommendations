$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#rec_id").val(res.id);
        $("#src_item_id").val(res.source_item_id);
        $("#tgt_item_id").val(res.target_item_id);
        $("#rec_type").val(res.recommendation_type);
        $("#rec_status").val(res.status);
        $("#rec_weight").val(res.recommendation_weight);
        $("#num_of_likes").val(res.number_of_likes);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#src_item_id").val("");
        $("#tgt_item_id").val("");
        $("#rec_type").val("");
        $("#rec_status").val("");
        $("#rec_weight").val("");
        $("#num_of_likes").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Recommendation
    // ****************************************

    $("#create-btn").click(function () {
        let src_item_id = parseInt($("#src_item_id").val());
        let tgt_item_id = parseInt($("#tgt_item_id").val());
        let type = $("#rec_type").val();
        let status = $("#rec_status").val();
        let weight = parseFloat($("#rec_weight").val());
        let likes = parseInt($("#num_of_likes").val());

        let data = {
            "source_item_id": src_item_id,
            "target_item_id": tgt_item_id,
            "recommendation_type": type,
            "status": status,
            "recommendation_weight": weight,
            "number_of_likes": likes
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: "/recommendations",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Recommendation
    // ****************************************

    $("#update-btn").click(function () {

        let rec_id = $("#rec_id").val();
        let src_item_id = parseInt($("#src_item_id").val());
        let tgt_item_id = parseInt($("#tgt_item_id").val());
        let type = $("#rec_type").val();
        let status = $("#rec_status").val();
        let weight = parseFloat($("#rec_weight").val());
        let likes = parseInt($("#num_of_likes").val());

        let data = {
            "source_item_id": src_item_id,
            "target_item_id": tgt_item_id,
            "recommendation_type": type,
            "status": status,
            "recommendation_weight": weight,
            "number_of_likes": likes
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/recommendations/${rec_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Recommendation
    // ****************************************

    $("#retrieve-btn").click(function () {

        let rec_id = $("#rec_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/recommendations/${rec_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function (res) {
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Recommendation
    // ****************************************

    $("#delete-btn").click(function () {

        let rec_id = $("#rec_id").val();

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/recommendations/${rec_id}`,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function (res) {
            clear_form_data()
            flash_message("Recommendation has been deleted!")
        });

        ajax.fail(function (res) {
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#rec_id").val("");
        $("#flash_message").empty();
        clear_form_data()
    });

    // ****************************************
    // Search for a Recommendation
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#pet_name").val();
        let category = $("#pet_category").val();
        let available = $("#pet_available").val() == "true";

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/pets?${queryString}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">ID</th>'
            table += '<th class="col-md-2">Name</th>'
            table += '<th class="col-md-2">Category</th>'
            table += '<th class="col-md-2">Available</th>'
            table += '<th class="col-md-2">Gender</th>'
            table += '<th class="col-md-2">Birthday</th>'
            table += '</tr></thead><tbody>'
            let firstPet = "";
            for (let i = 0; i < res.length; i++) {
                let pet = res[i];
                table += `<tr id="row_${i}"><td>${pet.id}</td><td>${pet.name}</td><td>${pet.category}</td><td>${pet.available}</td><td>${pet.gender}</td><td>${pet.birthday}</td></tr>`;
                if (i == 0) {
                    firstPet = pet;
                }
            }
            table += '</tbody></table>';
            $("#search_results").append(table);

            // copy the first result to the form
            if (firstPet != "") {
                update_form_data(firstPet)
            }

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });

    });

})
