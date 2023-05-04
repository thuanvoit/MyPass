let pageCodeSentBack = "";
let item_ID = "";
let note_url_ID = "";

function resetForm() {
  document.getElementById("addForm").reset();
}

function checkThis() {
  card_input = document.getElementById("id_card_number");
  card_input.onkeyup = function () {
    fetch(`/checkCard`, {
        method: "PUT",
        body: JSON.stringify({
          card_number: card_input.value,
        }),
      })
      .then((response) => response.json())
      .then((result) => {
        if (result["status"]) {
          card_input.style.borderWidth = "2px";
          card_input.style.borderColor = "green";
        } else {
          card_input.style.borderWidth = "2px";
          card_input.style.borderColor = "red";
        }
      });
  };
}

function reviewPassword(id) {

  password_field = document.getElementById("password-view-"+id)

  fetch(`/getpassword/${id}`, {
    method: "PUT",
    body: JSON.stringify({
    }),
  })
  .then((response) => response.json())
  .then((result) => {
    password_field.value = result['domain_password']
  });
}

function reviewCard(id) {
  card_number_field = document.getElementById("card-number-view-"+id)
  security_code_field = document.getElementById("security-code-view-"+id)
  expiration_field = document.getElementById("expiration-view-"+id)


  fetch(`/getcard/${id}`, {
    method: "PUT",
    body: JSON.stringify({
    }),
  })
  .then((response) => response.json())
  .then((result) => {
    card_number_field.value = result['card_number']
    security_code_field.value = result['security_code']
    expiration_field.value = result['expiration']

  });
}

function reviewBankAccount(id) {
  routing_number_field = document.getElementById("routing-number-view-"+id)
  account_number_field = document.getElementById("account-number-view-"+id)
  pin_number_field = document.getElementById("pin-number-view-"+id)


  fetch(`/getbankaccount/${id}`, {
    method: "PUT",
    body: JSON.stringify({
    }),
  })
  .then((response) => response.json())
  .then((result) => {
    routing_number_field.value = result['routing_number']
    account_number_field.value = result['account_number']
    pin_number_field.value = result['pin_number']

  });
}

function saveEditAccount(user) {
  user_current_last_name = document.getElementById(
    "user-current-last-name"
  ).value;
  user_current_first_name = document.getElementById(
    "user-current-first-name"
  ).value;
  user_current_email = document.getElementById("user-current-email").value;

  fetch(`/editAccountInfo`, {
      method: "PUT",
      body: JSON.stringify({
        user: user,
        user_current_last_name: user_current_last_name,
        user_current_first_name: user_current_first_name,
        user_current_email: user_current_email,
      }),
    })
    .then((response) => response.json())
    .then((result) => {
      if (result["status"] == 406) {
        parent = document.getElementById("modal-body-edit-info");
        if (document.getElementById("modal-alert-danger")) {
          document.getElementById("modal-alert-danger").remove();
        }
        new_alert = create_element(
          "div",
          "alert alert-danger",
          "modal-alert-danger",
          result["message"]
        );
        parent.append(new_alert);
      } else if (result["status"] == 200) {
        document.location.reload();
      }
    });
}

function changePassword(user) {
  current_password = document.getElementById("current-password").value;
  new_password = document.getElementById("new-password").value;
  confirmation = document.getElementById("new-password-confirm").value;

  fetch(`/changePassword`, {
      method: "PUT",
      body: JSON.stringify({
        user: user,
        current_password: current_password,
        new_password: new_password,
        confirmation: confirmation,
      }),
    })
    .then((response) => response.json())
    .then((result) => {
      if (result["status"] == 406) {
        parent = document.getElementById("modal-body-new-password");
        if (document.getElementById("modal-alert-danger")) {
          document.getElementById("modal-alert-danger").remove();
        }
        new_alert = create_element(
          "div",
          "alert alert-danger",
          "modal-alert-danger",
          result["message"]
        );
        parent.append(new_alert);
      } else if (result["status"] == 200) {
        document.location.reload();
      }
    });
}

function deleteAccount(user) {
  current_password = document.getElementById("user-current-password").value;

  fetch(`/deleteAccount`, {
      method: "PUT",
      body: JSON.stringify({
        user: user,
        current_password: current_password,
      }),
    })
    .then((response) => response.json())
    .then((result) => {
      if (result["status"] == 406) {
        parent = document.getElementById("modal-body-delete-account");
        if (document.getElementById("modal-alert-danger")) {
          document.getElementById("modal-alert-danger").remove();
        }
        new_alert = create_element(
          "div",
          "alert alert-danger",
          "modal-alert-danger",
          result["message"]
        );
        parent.append(new_alert);
      } else if (result["status"] == 200) {
        window.location.href = result["direction"];
      }
    });
}

function showOption(id) {
  document.getElementById("btn-fav-delete-group-" + id).style.display = "block";
  document.getElementById("btn-show-option-" + id).style.display = "none";
}

function hideTrash(id) {
  document.getElementById("btn-fav-delete-group-" + id).style.display = "none";
  document.getElementById("btn-show-option-" + id).style.display = "block";
}


function openLink(link) {
  if (link.startsWith("http://") || link.startsWith("https://")) {
    window.open(link, "_blank");
  } else {
    window.open(`http://${link}`, "_blank");
  }
}

function newItem() {
  document.getElementById("save-button").style.display = "block";
  document.getElementById("edit-button").style.display = "none";
}

function editIt(id, pageCode) {
  document.getElementById("save-button").style.display = "none";
  document.getElementById("edit-button").style.display = "block";

  resetForm();

  fetch(`/getit/${pageCode}/${id}`, {
      method: "PUT",
      body: JSON.stringify({}),
    })
    .then((response) => response.json())
    .then((result) => {

      if (pageCode == "password_view") {
        item_ID = result["id"];
        document.getElementById("id_url").value = result["url"];
        document.getElementById("id_domain_username").value =
          result["domain_username"];
        document.getElementById("id_domain_password").value =
          result["domain_password"];
        document.getElementById("id_note").value = result["note"];
        document.getElementById("flexCheckDefault").checked =
          result["favorite"];
        pageCodeSentBack = result["pageCode"];
      } else if (pageCode == "note_view") {
        item_ID = result["id"];
        note_url_ID = result["share_url"];
        document.getElementById("id_note_name").value = result["name"];
        document.getElementById("id_note").value = result["note"];
        document.getElementById("flexCheckDefault").checked =
          result["favorite"];
        document.getElementById("shareCheckBox").checked = result["share"];
        pageCodeSentBack = result["pageCode"];
      } else if (pageCode == "address_view") {
        item_ID = result["id"];
        document.getElementById("id_first_name").value = result["first_name"];
        document.getElementById("id_middle_name").value = result["middle_name"];
        document.getElementById("id_last_name").value = result["last_name"];
        document.getElementById("id_address").value = result["address"];
        document.getElementById("id_city").value = result["city"];
        document.getElementById("id_state").value = result["state"];
        document.getElementById("id_zipcode").value = result["zipcode"];
        document.getElementById("id_email").value = result["email"];
        document.getElementById("id_phone").value = result["phone"];
        document.getElementById("id_note").value = result["note"];
        document.getElementById("flexCheckDefault").checked =
          result["favorite"];
        document.getElementById("shareCheckBox").checked = result["share"];
        pageCodeSentBack = result["pageCode"];
      } else if (pageCode == "card_view") {
        item_ID = result["id"];
        document.getElementById("id_card_name").value = result["card_name"];
        document.getElementById("id_card_number").value = result["card_number"];
        document.getElementById("id_security_code").value =
          result["security_code"];
        document.getElementById("id_expiration_date").value =
          result["expiration"];
        document.getElementById("id_note").value = result["note"];
        document.getElementById("flexCheckDefault").checked =
          result["favorite"];
        pageCodeSentBack = result["pageCode"];
      } else if (pageCode == "bankaccount_view") {
        item_ID = result["id"];
        document.getElementById("id_bank_name").value = result["bank_name"];
        document.getElementById("id_bank_type").value = result["account_type"];
        document.getElementById("id_routing_number").value =
          result["routing_number"];
        document.getElementById("id_account_number").value =
          result["account_number"];
        document.getElementById("id_pin_number").value = result["pin_number"];
        document.getElementById("id_address").value = result["branch_address"];
        document.getElementById("id_phone").value = result["phone"];
        document.getElementById("id_note").value = result["note"];
        document.getElementById("flexCheckDefault").checked =
          result["favorite"];
        pageCodeSentBack = result["pageCode"];
      }
    });
}

function saveEditItem() {
  encoded_body = {};

  if (pageCodeSentBack == "password_view") {
    // START
    url = document.getElementById("id_url").value;
    domain_username = document.getElementById("id_domain_username").value;
    domain_password = document.getElementById("id_domain_password").value;
    note = document.getElementById("id_note").value;
    favorite = document.getElementById("flexCheckDefault").checked;

    encoded_body = JSON.stringify({
      url: url,
      domain_username: domain_username,
      domain_password: domain_password,
      note: note,
      favorite: favorite,
    });
    // END
  } else if (pageCodeSentBack == "note_view") {
    // START
    note_name = document.getElementById("id_note_name").value;
    note = document.getElementById("id_note").value;
    favorite = document.getElementById("flexCheckDefault").checked;
    share = document.getElementById("shareCheckBox").checked;

    encoded_body = JSON.stringify({
      note_name: note_name,
      note: note,
      favorite: favorite,
      share: share,
    });
    // END
  } else if (pageCodeSentBack == "address_view") {
    // START
    first_name = document.getElementById("id_first_name").value;
    middle_name = document.getElementById("id_middle_name").value;
    last_name = document.getElementById("id_last_name").value;
    address = document.getElementById("id_address").value;
    city = document.getElementById("id_city").value;
    state = document.getElementById("id_state").value;
    zipcode = document.getElementById("id_zipcode").value;
    email = document.getElementById("id_email").value;
    phone = document.getElementById("id_phone").value;
    note = document.getElementById("id_note").value;
    favorite = document.getElementById("flexCheckDefault").checked;
    share = document.getElementById("shareCheckBox").checked;

    encoded_body = JSON.stringify({
      first_name: first_name,
      middle_name: middle_name,
      last_name: last_name,
      address: address,
      city: city,
      state: state,
      zipcode: zipcode,
      email: email,
      phone: phone,
      note: note,
      share: share,
      favorite: favorite,
    });
    // END
  } else if (pageCodeSentBack == "card_view") {
    // START
    card_name = document.getElementById("id_card_name").value;
    card_number = document.getElementById("id_card_number").value;
    security_code = document.getElementById("id_security_code").value;
    expiration_date = document.getElementById("id_expiration_date").value;
    note = document.getElementById("id_note").value;
    favorite = document.getElementById("flexCheckDefault").checked;

    encoded_body = JSON.stringify({
      card_name: card_name,
      card_number: card_number,
      security_code: security_code,
      expiration_date: expiration_date,
      note: note,
      favorite: favorite,
    });
    // END
  } else if (pageCodeSentBack == "bankaccount_view") {
    // START
    bank_name = document.getElementById("id_bank_name").value;
    bank_type = document.getElementById("id_bank_type").value;
    routing_number = document.getElementById("id_routing_number").value;
    account_number = document.getElementById("id_account_number").value;
    pin_number = document.getElementById("id_pin_number").value;
    address = document.getElementById("id_address").value;
    phone = document.getElementById("id_phone").value;
    note = document.getElementById("id_note").value;
    favorite = document.getElementById("flexCheckDefault").checked;

    encoded_body = JSON.stringify({
      bank_name: bank_name,
      bank_type: bank_type,
      routing_number: routing_number,
      account_number: account_number,
      pin_number: pin_number,
      address: address,
      phone: phone,
      note: note,
      favorite: favorite,
    });
    // END
  }

  fetch(`/saveEditItem/${pageCodeSentBack}/${item_ID}`, {
      method: "POST",
      body: encoded_body,
    })
    .then((response) => response.json())
    .then((result) => {
      resetForm();
      document.location.reload();
    });
}

function starIt(id, pageCode) {
  fetch(`/star/${pageCode}/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        stared: true,
      }),
    })
    .then((response) => response.json())
    .then((result) => {
      if (result["favorite"]) {
        parent = document.getElementById("btn-star-" + id);
        parent.innerHTML = "";
        new_btn_star = create_element("i", "bi bi-star-fill", "", "");
        parent.append(new_btn_star);

        card_border = document.getElementById("card-border-" + id);
        card_border.className = "card border-warning";
      } else {
        parent = document.getElementById("btn-star-" + id);
        parent.innerHTML = "";
        new_btn_star = create_element("i", "bi bi-star", "", "");
        parent.append(new_btn_star);

        card_border = document.getElementById("card-border-" + id);
        card_border.className = "card";
      }
    });
}

function deleteIt(id, pageCode) {
  fetch(`/delete_item/${pageCode}/${id}`, {
      method: "POST",
      body: JSON.stringify({
        id: id,
        pageCode: pageCode,
      }),
    })
    .then((response) => response.json())
    .then((result) => {
      document.location.reload();
    });
}

function create_element(type, classname, idname, textcontent) {
  var new_element = document.createElement(type);
  if (classname != "") {
    new_element.className = classname;
  }
  if (idname != "") {
    new_element.id = idname;
  }
  if (textcontent != "") {
    new_element.innerHTML = textcontent;
  }
  return new_element;
}

function copy(id, content) {
  fetch(`/getpassword/${id}`, {
      method: "GET",
    })
    .then((response) => response.json())
    .then((result) => {
      if (content == "username") {
        copyContent(result["domain_username"]);
      } else if (content == "password") {
        copyContent(result["domain_password"]);
      }
    });
}

function copyContent(content) {
  fetch(`/copyit`, {
      method: "PUT",
      body: JSON.stringify({
        content: content,
      }),
    })
    .then((response) => response.json())
    .then((result) => {
    });
}