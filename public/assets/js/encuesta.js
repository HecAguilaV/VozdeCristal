// Control de encuesta respondida via localStorage
(function() {
  const STORAGE_KEY = 'vozdecristal_encuesta_respondida';
  const botonEncuesta = document.querySelector('a[href="/encuesta"]');
  
  if (!botonEncuesta) return;

  // Verificar si ya respondió
  const yaRespondio = localStorage.getItem(STORAGE_KEY);
  
  if (yaRespondio) {
    // Cambiar texto y estilo del botón
    botonEncuesta.innerHTML = '¿Editar tu respuesta? →';
    botonEncuesta.classList.add('opacity-70');
    
    // Agregar mensaje de agradecimiento
    const mensajeGracias = document.createElement('p');
    mensajeGracias.className = 'text-sm opacity-60 mt-2';
    mensajeGracias.textContent = '✓ Ya respondiste esta encuesta. Gracias por tu participación.';
    botonEncuesta.parentElement.appendChild(mensajeGracias);
  }
  
  // NO marcamos aquí - solo el iframe al enviarse lo hará
})();

// Detectar cuando el iframe de Google Forms se envía (truco del onload)
(function() {
  const iframe = document.getElementById('formIframe');
  if (!iframe) return;
  
  let cargaInicial = true;
  
  iframe.addEventListener('load', function() {
    // Primera carga: mostrar formulario (ignorar)
    if (cargaInicial) {
      cargaInicial = false;
      return;
    }
    
    // Segunda carga: usuario envió el formulario
    const timestamp = new Date().toISOString();
    localStorage.setItem('vozdecristal_encuesta_respondida', timestamp);
    
    // Opcional: Mostrar mensaje de confirmación
    console.log('✓ Encuesta enviada y registrada');
  });
})();
