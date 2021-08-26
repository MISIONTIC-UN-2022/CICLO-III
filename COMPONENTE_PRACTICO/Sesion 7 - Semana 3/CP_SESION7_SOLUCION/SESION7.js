function validar_formulario() {
  var usuario = document.formRegistro.usuario;
  var email = document.formRegistro.email;
  var password = document.formRegistro.password;

  var usuario_len = usuario.value.length;
  if (usuario_len == 0 || usuario_len < 8) {
    alert("Debes ingresar un usuario con min. 8 caracteres");
    passid.focus();
    return false; //Para la parte dos, que los datos se conserven
  }

  var formato_email = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (!email.value.match(formato_email)) {
    alert("Debes ingresar un email electronico valido!");
    email.focus();
    return false; //Para la parte dos, que los datos se conserven
  }

  var passid_len = password.value.length;
  if (passid_len == 0 || passid_len < 8) {
    alert("Debes ingresar una password con mas de 8 caracteres");
    passid.focus();
  }
}
