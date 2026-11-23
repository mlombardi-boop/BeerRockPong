/**
 * BundesBirra · crea el formulario de inscripción y la planilla de respuestas.
 * Uso: pegar en script.google.com, guardar y ejecutar UNA sola vez la función crearFormulario.
 * Después agregar a mano la pregunta "Comprobante de pago" (tipo Subir archivo, obligatoria).
 * Para una nueva edición: actualizar el título, la fecha y los valores de abajo.
 */
const REGLAMENTO_URL = 'https://beerrock.vercel.app/#reglamento';  // cambiar si se renombra el proyecto en Vercel
const PRECIO = '$30.000 por persona ($90.000 por equipo de 3)';
const ALIAS = 'LA.BUNDES.BIRRA';

function crearFormulario() {
  const form = FormApp.create('BundesBirra · Inscripción Fecha 1');
  form.setDescription(
    'BundesBirra · La Bundes · Liga Argentina de Beerpong\n' +
    'Viernes 11 de diciembre · 19 hs · BABA Bar (Av. del Libertador 2629, Olivos)\n\n' +
    'Equipos de 3 con 3 partidos garantizados y una cheeseburger por jugador.\n\n' +
    'Inscripción: ' + PRECIO + '.\nTransferí al alias ' + ALIAS + '\n' +
    'Subí el comprobante al final del formulario.'
  );
  form.setProgressBar(true);
  form.setAllowResponseEdits(false);
  form.setConfirmationMessage(
    '¡Listo! Recibimos la inscripción. Te escribimos por WhatsApp para confirmar el lugar. El que pierde, toma.'
  );

  const celular = FormApp.createTextValidation()
    .setHelpText('Escribí solo números, con código de área. Ej: 11 5555 5555')
    .requireTextMatchesPattern('^[0-9 +()-]{8,20}$')
    .build();
  const email = FormApp.createTextValidation()
    .setHelpText('Revisá el email.')
    .requireTextIsEmail()
    .build();

  form.addSectionHeaderItem().setTitle('Integrante 1 (capitán)');
  form.addTextItem().setTitle('Integrante 1: nombre y apellido').setRequired(true);
  form.addTextItem().setTitle('Integrante 1: celular con WhatsApp')
    .setHelpText('Es el contacto del equipo.').setValidation(celular).setRequired(true);

  form.addSectionHeaderItem().setTitle('Integrante 2');
  form.addTextItem().setTitle('Integrante 2: nombre y apellido').setRequired(true);

  form.addSectionHeaderItem().setTitle('Integrante 3');
  form.addTextItem().setTitle('Integrante 3: nombre y apellido').setRequired(true);

  form.addTextItem().setTitle('Email de contacto').setValidation(email).setRequired(true);
  form.addCheckboxItem().setTitle('Mayores de edad')
    .setChoiceValues(['Los 3 integrantes somos mayores de 18 años']).setRequired(true);
  form.addCheckboxItem().setTitle('Reglamento')
    .setHelpText('Leelo acá: ' + REGLAMENTO_URL)
    .setChoiceValues(['Leímos y aceptamos el reglamento']).setRequired(true);

  const ss = SpreadsheetApp.create('BundesBirra · Inscriptos Fecha 1');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('Link para la web (FORM_URL): ' + form.getPublishedUrl());
  Logger.log('Editar el formulario: ' + form.getEditUrl());
  Logger.log('Planilla de respuestas: ' + ss.getUrl());
}
