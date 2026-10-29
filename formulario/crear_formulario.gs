/**
 * Beer Rock · crea el formulario de inscripción y la planilla de respuestas.
 * Uso: pegar en script.google.com, guardar y ejecutar UNA sola vez la función crearFormulario.
 * Después agregar a mano la pregunta "Comprobante de pago" (tipo Subir archivo, obligatoria).
 * Para una nueva edición: actualizar el título, la fecha y los valores de abajo.
 */
const REGLAMENTO_URL = 'https://beerrock.vercel.app/#reglamento';
const PRECIO = '$40.000 por persona ($120.000 por equipo de 3)';
const ALIAS = 'BEER.ROCK.PONG';

function crearFormulario() {
  const form = FormApp.create('Beer Rock · Inscripción 1ª edición');
  form.setDescription(
    'Torneo de beer pong · Equipos de 3\n' +
    'Sábado 21 de noviembre · 19 hs · Cuba Fátima\n\n' +
    'Inscripción: ' + PRECIO + '. Transferí al alias ' + ALIAS +
    ' y subí el comprobante al final del formulario. Sin comprobante, el equipo no queda inscripto.\n\n' +
    'Quedan pocos cupos.'
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

  form.addTextItem().setTitle('Nombre del equipo').setRequired(true);

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

  const ss = SpreadsheetApp.create('Beer Rock · Inscriptos 1ª edición');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  Logger.log('Link para la web (FORM_URL): ' + form.getPublishedUrl());
  Logger.log('Editar el formulario: ' + form.getEditUrl());
  Logger.log('Planilla de respuestas: ' + ss.getUrl());
}
