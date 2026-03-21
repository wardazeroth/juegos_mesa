function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

document.addEventListener('DOMContentLoaded', function() {
    const btnToggle = document.querySelector('.toggle-btn')

    if (btnToggle) {
        btnToggle.addEventListener('click', function () {
            document.getElementById('sidebar').classList.toggle('active')
        })
    }

    const modalEliminar = document.getElementById('ModalEliminar');
    if (modalEliminar) {
        const myModalDelete = bootstrap.Modal.getOrCreateInstance(modalEliminar);
        const btnConfirmar = document.getElementById('btnConfirmarEliminar');
        const tituloModal = document.getElementById('tituloModal');
        const mensajeModal = document.getElementById('mensajeModal');

        document.addEventListener('click', function(e) {
            const boton = e.target.closest('.btn-abrir-eliminar');
            if (boton) {
                e.preventDefault();
            const urlEliminar = boton.getAttribute('data-url');
            const tipoElemento = boton.getAttribute('data-tipo');

            tituloModal.innerText = `Eliminar ${tipoElemento}`;
            mensajeModal.innerText = `¿Estás seguro de que deseas eliminar ${tipoElemento}?`;

            btnConfirmar.href = urlEliminar;

            myModalDelete.show();
            }
        });
    }
    try {
    const particlesContainer = document.getElementById('particles-js');
    if (particlesContainer && typeof particlesJS !== 'undefined') {
        particlesJS('particles-js', {
            "particles": {
                "number": { "value": 150, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#ffffff" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.3, "random": true },
                "size": { "value": 3, "random": true },
                "line_linked": { "enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.7, "width": 1 },
                "move": { "enable": true, "speed": 6, "out_mode": "out" }
            },
            "interactivity": {
                "events": {
                    "onhover": { "enable": true, "mode": "repulse" },
                    "onclick": { "enable": true, "mode": "push" }
                }
            },
            "retina_detect": true
        });
        console.log("Partículas inicializadas con éxito.");
    }
    } catch (e) {
        console.warn("ParticlesJS no pudo cargar, pero el resto sigue funcionando:", e);
    }

    const btnNuevoPost = document.getElementById("nuevo_post");
    const modalCrearEl = document.getElementById('myModal');
    if (btnNuevoPost && modalCrearEl) {
        const myModalCrear = new bootstrap.Modal(modalCrearEl);
        btnNuevoPost.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Abriendo modal de nuevo post...");
            myModalCrear.show();
        });
    }

    const modalResponder = document.getElementById('ModalResponderPrincipal');
    const myModalResp = new bootstrap.Modal(modalResponder);
    if (modalResponder && myModalResp) {
        document.querySelectorAll('.responder').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault()

            myModalResp.show()
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('.reaccion').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            let comentarioId = this.dataset.id;
            let modelo= this.dataset.modelo;
            let likeIcon = this.querySelector('i'); //ícono del botón)
            let likeCount = this.querySelector('.reaction-text');

            fetch(`/foro/${modelo}/${comentarioId}/like`, {
                method: 'POST',
                headers: {
                "X-CSRFToken": getCSRFToken(), // Necesario para Django
                "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                // Actualizar el número de likes
                likeCount.textContent = data.total_likes;

                //Cambiar la clase del ícono
                if (data.liked) {
                    likeIcon.classList.remove('fa-regular');
                    likeIcon.classList.add('fa-solid');
                }else {
                    likeIcon.classList.remove('fa-solid');
                    likeIcon.classList.add('fa-regular');
                }
            })
            .catch(error =>console.error('Error:', error));
        });
    });
});

const imagenes_resp = document.getElementById('imagenes')
const prev_resp = document.getElementById('previsual_resp')
const fomularioRespuesta = document.getElementById('formulario')

let agregar_img = []
let elim_resp = []
if (imagenes_resp) {
    imagenes_resp.addEventListener('change', () => {
        let archivos = imagenes_resp.files
        for (let i=0; i < archivos.length; i++) {
            
            console.log('hay lista: ', agregar_img)
            const file = archivos[i]
            const reader = new FileReader();    
            const container = document.createElement('div');
            container.classList.add('imagen-container')
            const img = document.createElement('img');
            const trashIcono = document.createElement('i')
            trashIcono.classList.add('fas', 'fa-trash-alt', 'borrar-icon')

        trashIcono.addEventListener('click', function() {
            container.remove();
            elim_resp.push(archivos[i])
            console.log('eliminando: ', elim_resp)
        })

        reader.onload = function(e) {
            // convert image file to base64 string
            img.src = reader.result
            container.appendChild(img)
            container.appendChild(trashIcono)
            prev_resp.appendChild(container)
            prev_resp.style.display = 'block';
            agregar_img.push(archivos[i])

            console.log('cargadas para enviar', agregar_img)
            let dataTransfer = new DataTransfer()
            for (let file of agregar_img) {
                dataTransfer.items.add(file)
            }
            imagenes_resp.files = dataTransfer.files
        }
        reader.readAsDataURL(archivos[i]);
        }
    });
}

const btn_add_img = document.getElementById('add_img')

if (btn_add_img) {
    btn_add_img.addEventListener('click', function (e) {
    if (typeof imagenes_resp !== 'undefined') {
            imagenes_resp.click();
        }
    });
}

if (fomularioRespuesta) {

    fomularioRespuesta.addEventListener('submit', function enviarForm(e) {
        const id = this.dataset.id;
        console.log('eliminadas: ', elim_resp);
        let form = e.target                  
        let formData = new FormData(form);

        formData.append('imagenes_eliminadas', JSON.stringify(elim_resp));

        fetch(`/foro/${modelo}/${id}/edit-foto`,  {
        method: 'POST',
        body: formData,
        headers: {
        "X-CSRFToken": getCSRFToken(),
        "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('imágenes actualizadas')
    })
    .catch(error=> {
        console.log('Error:', error)});   
    });
}

    document.querySelectorAll('.citar').forEach(button => {
        button.addEventListener('click', function(event) {
        event.preventDefault();

        const modalElement = document.getElementById('ModalResponderPrincipal');
        const instanciaModal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);           
        instanciaModal.show()

        let contenidoCita = this.dataset.texto;

        let modelo = this.dataset.modelo
        let autorCita = this.dataset.autor;
        let cita = `${autorCita}:\n${contenidoCita}\n`

        if (modelo == 'Post') {
            let post_id = this.dataset.postid || None;
            document.getElementById('post_cita').value = post_id

            let citaTexto = document.getElementById('post-cita')
            citaTexto.style.display='block';
            citaTexto.querySelector('pre').textContent = cita
        } else {
            let comentario_id = this.dataset.comentarioid || None;
            document.getElementById('comentario_cita').value = comentario_id

            let citaTexto= document.getElementById('comentario-cita')
            citaTexto.style.display='block';
            citaTexto.querySelector('pre').textContent = cita
        }
    });
});

let imagenes_list = []
const imagenes = document.getElementById('imagenes')
if (imagenes) {
imagenes.addEventListener('change', function(event) {        
    let imagenes = event.target.files;
    let previsual = document.getElementById('imagen-prev')

    for (let i=0; i < imagenes.length; i++) {
        const file = imagenes[i]
        const reader = new FileReader();
        const container = document.createElement('div');
        container.classList.add('imagen-container')

        console.log(imagenes_list)  

        const img = document.createElement('img');
        const trashIcono = document.createElement('i')
        trashIcono.classList.add('fas', 'fa-trash-alt', 'borrar-icon')

        trashIcono.addEventListener('click', function() {
            container.remove();
    
            console.log(imagenes_list)
            imagenes_list = imagenes_list.filter(f => f !== file)
            let dataTransfer = new DataTransfer()
            for (let f of imagenes_list) {
                dataTransfer.items.add(f)
            }

            document.getElementById('imagenes').files = dataTransfer.files
        })

        reader.onload = function(e) {
            // convert image file to base64 string
            img.src = reader.result
            container.appendChild(img)
            container.appendChild(trashIcono)
            previsual.appendChild(container)

            previsual.style.display = 'block';
            imagenes_list.push(imagenes[i])

            let dataTransfer = new DataTransfer()
            for (let file of imagenes_list) {
                dataTransfer.items.add(file)
            }
            document.getElementById('imagenes').files = dataTransfer.files
        }
        reader.readAsDataURL(imagenes[i]);
    }
    });
}


document.addEventListener('DOMContentLoaded', function () {    
    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('add-img-edit')) {
            event.preventDefault();
            images = document.getElementById('imagenes_edit')
            
            const form = event.target.closest('form');
            const input = form.querySelector('.imagenes-edit');
            if (input) {
                input.click();
            }
        }
    });
});

    document.querySelectorAll('.edit-post').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            let postId = this.dataset.id;
            let formularioEdicionPost = document.getElementById('edit-form');
            let extra = document.getElementById('extra')
            let modelo = this.dataset.modelo
            let imagenes_edit = document.getElementById('imagenes_edit_post')
            let previsual = document.getElementById('imagen-prev-edit-post')
            
            abrirEditorComentario({ modelo: modelo, id: postId, formularioEdicion: formularioEdicionPost, extra: extra, imagenes_edit: imagenes_edit, previsual: previsual });
    });
});

document.querySelectorAll('.edit-comment').forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        let comentarioId = this.dataset.id;
        let formularioEdicionComment = document.getElementById(`edit-comment-form-${comentarioId}`);
        let extra = document.getElementById(`extra-2-${comentarioId}`)
        let modelo = this.dataset.modelo
        let imagenes_edit = document.getElementById(`imagenes_edit-${comentarioId}`)
        let previsual = document.getElementById(`imagen-prev-edit-${comentarioId}`)

        abrirEditorComentario({ modelo: modelo, id: comentarioId, formularioEdicion: formularioEdicionComment, extra: extra, imagenes_edit: imagenes_edit, previsual: previsual });
    });
});

window.abrirEditorComentario= function({modelo, id, formularioEdicion, extra, imagenes_edit, previsual}) {
    if (formularioEdicion) {
            formularioEdicion.style.display='block'
            extra.style.display='none'            
        } else {
            console.error(`No se encontró el formulario para el comentario con ID: ${id}`);
        }
        let imagenes_add = []
        let eliminar_img= []

        obtener_imagenes_backend({modelo: modelo, id:id, previsual:previsual, eliminar_img: eliminar_img});

        imagenes_edit.addEventListener('change', () => {
            let archivos = imagenes_edit.files
            for (let i=0; i < archivos.length; i++) {
                
                console.log('hay lista: ', imagenes_add)
                const file = archivos[i]
                const reader = new FileReader();
                const container = document.createElement('div');
                container.classList.add('imagen-container')
                const img = document.createElement('img');
                const trashIcono = document.createElement('i')
                trashIcono.classList.add('fas', 'fa-trash-alt', 'borrar-icon')

            trashIcono.addEventListener('click', function() {
                container.remove();

            })

            reader.onload = function(e) {
                // convert image file to base64 string
                img.src = reader.result
                container.appendChild(img)
                container.appendChild(trashIcono)
                previsual.appendChild(container)
                previsual.style.display = 'block';
                imagenes_add.push(archivos[i])

                console.log('cargadas para enviar', imagenes_add)
                let dataTransfer = new DataTransfer()
                for (let file of imagenes_add) {
                    dataTransfer.items.add(file)
                }
                imagenes_edit.files = dataTransfer.files
            }
            reader.readAsDataURL(archivos[i]);
            }
        })

            formularioEdicion.addEventListener('submit', function enviarForm(e) {
                console.log('eliminadas: ', eliminar_img);
                let form = e.target                  
                let formData = new FormData(form);

                formData.append('imagenes_eliminadas', JSON.stringify(eliminar_img));

                fetch(`/foro/${modelo}/${id}/edit-foto`,  {
                method: 'POST',
                body: formData,
                headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('imágenes actualizadas')
            })
            .catch(error=> {
                console.log('Error:', error)});   
        });
}

function obtener_imagenes_backend({modelo, id, previsual, eliminar_img}) {
    fetch(`/foro/${modelo}/${id}/edit-foto`,  {
                method: 'GET',
                headers: {
                "X-CSRFToken": getCSRFToken(),
                "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                let images = data.imagenes
                
                if (images) {
                    for (let imgData of images) {
                        const container = document.createElement('div');
                        container.classList.add('imagen-container')

                        const img = document.createElement('img');
                        if (imgData['tipo'] == 'file') {
                            img.src =  `/media/${imgData.src}`
                        } else {
                            img.src = imgData.src
                        }
                        
                        const trashIcono = document.createElement('i')
                        trashIcono.classList.add('fas', 'fa-trash-alt', 'borrar-icon')
                        container.appendChild(img)
                        container.appendChild(trashIcono)
                        previsual.appendChild(container)

                        previsual.style.display = 'block';

                        trashIcono.addEventListener('click', function() {
                            container.remove();
                            eliminar_img.push(imgData)
                            console.log("Lista actual de eliminadas:", eliminar_img);                       
                    })
            }
        }
    }).catch(error =>console.error('Error:', error));
}       

document.querySelectorAll('.add_url_btn').forEach(btn => {
    btn.addEventListener('click', function(e){
        e.preventDefault();
        const id = this.dataset.id;

        bloque = document.querySelector(`.add_url_com[data-id="${id}"]`)
        if (bloque) {
            bloque.style.display = 'block';
        }
    })
});

document.querySelectorAll('.add-link-com').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        const id= this.dataset.id;
        console.log('holaaa chwee')
        let add_link_com = document.querySelector(`.add-link-com-cuadro[data-id="${id}"]`)
        add_link_com.style.display = 'block'
    })
})

document.getElementById('add_url').addEventListener('click', function(e){
    e.preventDefault();
    let url_add =document.querySelector('.add_url');
    url_add.style.display = 'block';
})

document.addEventListener('DOMContentLoaded', () => {
    const addLinkPost = document.getElementById('add-link-post')

    if (addLinkPost) {
        addLinkPost.addEventListener('click', function(e) {
            e.preventDefault();
            let add_link_post = document.querySelector('.add-link-post');
            add_link_post.style.display = 'block';
        })
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const addLink = document.getElementById('add-link')
    if (addLink) {
        addLink.addEventListener('click', function(e) {
            e.preventDefault();
            let add_link = document.querySelector('.add-link');
            add_link.style.display = 'block';
        })
    }
})

document.addEventListener('DOMContentLoaded', () => {
    const addUrlPost = document.getElementById('add_url_post')

    if (addUrlPost) {
        addUrlPost.addEventListener('click', function(e) {
            e.preventDefault();
            let url_add =document.querySelector('.add_url_post');
            url_add.style.display = 'block';
        })
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input[type="url"]');
    const inputs_file = document.querySelectorAll('input[type="file"]')

    inputs.forEach((input) =>{
        input.addEventListener('input', (event) => {
            const inputId = event.target.id
            const dataId = event.target.dataset.id
            const modelo = event.target.dataset.model
            let inputPrincipal = null
            let previsual_form = null
            let inputLink = null
            let prevLink = null

            if (modelo === 'post') {
                inputPrincipal = document.getElementById('url_post')
                previsual_form = document.getElementById('imagen-prev-edit-post')
                inputLink = document.getElementById('link-post')
                prevLink = document.getElementById("link-prev-post")
                
            } else if (modelo === 'comentario') {
                inputPrincipal = document.getElementById(`url_com_${dataId}`)
                previsual_form = document.getElementById(`imagen-prev-edit-${dataId}`)
                inputLink = document.getElementById(`link-com-${dataId}`)
                prevLink = document.getElementById(`link-prev-edit-${dataId}`)
            } else if(modelo === 'respuesta') {
                inputPrincipal = document.getElementById('url')
                previsual_form = document.getElementById('previsual_resp')
                inputLink = document.getElementById('link-resp')
                prevLink = document.getElementById('link-prev-resp')
            }
            
        previsual_form.style.display = 'block';
        const url = inputPrincipal.value;
        const link = inputLink.value;
        prevLink.style.display = 'block'
        const linked = `<a href="${link}" target="_blank">${link}</a>`
        prevLink.innerHTML = linked

        if (!url) return;

        const container = document.createElement('div');
        container.classList.add('imagen-container')
        const img = document.createElement('img');
        img.src = url;

        const trashIcono = document.createElement('i')
        trashIcono.classList.add('fas', 'fa-trash-alt', 'borrar-icon')

        trashIcono.addEventListener('click', function() {
            container.remove();
            input.value = '';
            })
            container.appendChild(img)
            container.appendChild(trashIcono)
            previsual_form.appendChild(container)
            previsual_form.style.display = 'block';
            })
        })
    });

document.addEventListener('DOMContentLoaded', () => {
    const inputs_file = document.querySelectorAll('input[type="file"]')

    inputs_file.forEach((input) =>{
        input.addEventListener('input', (event) => {
            const inputId = event.target.id     
            const dataId = event.target.dataset.id
            const modelo = event.target.dataset.model
            let inputAdjunto = null
            let prevFile = null
            const extensionesValidas =['.jpg', '.png', '.pdf', '.txt', '.zip', '.docx'];

            if (modelo == 'post') {
                inputAdjunto = document.getElementById('archivo_post')
                prevFile = document.getElementById("file-prev-post")
            }
            else if (modelo == 'comentario') {
                inputAdjunto = document.getElementById(`archivo_com-${dataId}`)
                prevFile = document.getElementById(`file-prev-com-${dataId}`)
            }else if(modelo === 'respuesta') {
                inputAdjunto = document.getElementById('archivo')
                prevFile = document.getElementById("file-prev-resp")
            }

        const archivos= inputAdjunto.files;
        Array.from(archivos).forEach((archivo) => {
            const extension = archivo.name.substring(archivo.name.lastIndexOf('.')).toLowerCase(); // Extrae .pdf, .jpg, etc.
            if (!extensionesValidas.includes(extension)) {
                alert(`Extensión ${extension} no permitida. Solo se aceptan ${extensionesValidas.join(', ')}`)
            } else {
                prevFile.style.display = 'block'
                const container = document.createElement('div');
                const icono = document.createElement('i');
                // <a href="{{ archivo.archivo.url }}" download>{{ archivo.archivo.name|cut:"adjuntos/" }}</a>
                if (extension == '.pdf') {
                    icono.classList.add('fas', 'fa-file-pdf')
                    icono.style.fontSize = '2rem'
                } else if (extension === '.jpg' || extension === '.jpeg' || extension === '.png') {
                    icono.classList.add('fas', 'fa-file-image');
                    icono.style.fontSize = '2rem'
                } else if (extension === '.txt') {
                    icono.classList.add('fas', 'fa-file-alt');
                    icono.style.fontSize = '2rem'
                }else if (extension === '.docx') {
                    icono.classList.add('fas', 'fa-file-word')
                    icono.style.fontSize = '2rem'
                }else if (extension === '.zip') {
                    icono.classList.add('fas', 'fa-file-zipper')
                    icono.style.fontSize = '2rem'
                } else {
                    icono.classList.add('fas', 'fa-file');
                    icono.style.fontSize = '2rem'
                }
                let nombre_archivo = archivo.name
                console.log('los adjuntos: ', archivo)
                container.appendChild(icono)
                prevFile.innerHTML = nombre_archivo
                prevFile.appendChild(container);
                }
            })
        })
    })
});

const formularioRespuesta = document.getElementById('formulario') || document.querySelector('.form-respuesta');

window.agregarCampo = function(event) {
    if (event) event.preventDefault();
    const boton = event.target.closest('a, button')
    const modelo = event.target.dataset.model
    const dataId = event.target.dataset.id

    const contenedorRaiz = boton.closest('.marco-editor, .marco, .modalResp, .modalPost, .modal-body');
    let previsual_form = null;
    const input = document.createElement('input')
    input.type = 'url';
    input.classList.add("form-control")
    input.style = "margin: 5px 5px; border-radius: 5px"
    input.placeholder = 'URL de imagen';

        if ( modelo === 'post') {
        contenedor = contenedorRaiz.querySelector('.add_url_post') || contenedorRaiz.querySelector('.add_url');
        previsual_form = document.getElementById('imagen-prev-edit-post')
        input.name = 'url_post';

        } else if ( modelo === 'comentario') {
        contenedor = contenedorRaiz.querySelector(`.add_url_com[data-id="${dataId}"]`);
        previsual_form = document.getElementById(`imagen-prev-edit-${dataId}`)
        input.name = 'url_com';
        
        } else if ( modelo === 'respuesta') {
        contenedor = contenedorRaiz.querySelector('div.add_url');
        previsual_form = document.getElementById('previsual_resp')
        input.name = 'url';
    }

    contenedor.appendChild(input)

    previsual_form.style.display = 'block';
    input.addEventListener('input', () => {
        const url = input.value;

        if (!url) return;

        const container = document.createElement('div');
        container.classList.add('imagen-container')
        const img = document.createElement('img');
        img.src = url;

        const trashIcono = document.createElement('i')
        trashIcono.classList.add('fas', 'fa-trash-alt', 'borrar-icon')

        trashIcono.addEventListener('click', function() {
            container.remove();
            input.value = '';
        })
            container.appendChild(img)
            container.appendChild(trashIcono)
            previsual_form.appendChild(container)
            previsual_form.style.display = 'block';
    }
)};

window.agregarLink = function(event) {
    const boton = event.target.closest('a, button');
    const modelo = event.target.dataset.model
    const dataId = event.target.dataset.id

    const contenedorRaiz = boton.closest('.marco-editor, .marco, .modalResp, modalPost');

    let previsual_form = null;
    let contenedor = null;
    const input = document.createElement('input')
    input.type = 'url';
    input.classList.add("form-control")
    input.style = "margin: 5px 5px; border-radius: 5px"
    input.placeholder = 'Inserte un nuevo link';
    if ( modelo === 'post') {
        contenedor = contenedorRaiz.querySelector('.add-link-post') || contenedorRaiz.querySelector('.add-link');
        previsual_form = document.getElementById('link-prev-post');
        previsual_form = document.getElementById('link-prev-post')
        input.name = 'link-post';

        } else if ( modelo === 'comentario') {
        contenedor = contenedorRaiz.querySelector(`.add-link-com-cuadro[data-id="${dataId}"]`);
        previsual_form = document.getElementById(`link-prev-edit-${dataId}`)
        input.name = 'link-com';
        
        } else if ( modelo === 'respuesta') {
        contenedor = contenedorRaiz.querySelector('div.add-link');
        previsual_form = document.getElementById("link-prev-resp")
        input.name = 'link-resp';
    }

    contenedor.appendChild(input)

    previsual_form.style.display = 'block';
    input.addEventListener('input', () => {
        const url = input.value;

        if (!url) return;

        const container = document.createElement('div');
        const enlace = document.createElement('a')
        enlace.href = url
        enlace.textContent = url;
        enlace.target = "_blank";
        container.appendChild(enlace)
        container.style = 'padding: 1rem 0'
        previsual_form.appendChild(container)
        previsual_form.style.display = 'block';
    });
}

const add_archivo = document.getElementById('add_archivo')
const add_archivo_post = document.getElementById('add_archivo_post')

if (add_archivo) {
    add_archivo.addEventListener('click', function(e) {
        e.preventDefault()
        let input_archivo = document.getElementById('archivo')
        input_archivo.click()
    });
}

if (add_archivo_post) {
    add_archivo_post.addEventListener('click', function(e) {
        e.preventDefault()
        let input_archivo = document.getElementById('archivo_post')
        input_archivo.click()
    });
}

document.querySelectorAll('.add_archivo_com').forEach(btn => {
    btn.addEventListener('click', function(e){
    e.preventDefault()
    const id= this.dataset.id;
    let input_archivo = document.getElementById(`archivo_com-${id}`)
    input_archivo.click()
    })
});

    const imagenes_edit = document.getElementById('imagenes_edit')
    const previsual = document.getElementById('imagen-prev-edit-post')
    const formularioEdicion = document.getElementById('post-form');

    let imagenes_add = []
    let eliminar_img= []

    imagenes_edit.addEventListener('change', () => {
        let archivos = imagenes_edit.files


        for (let i=0; i < archivos.length; i++) {
            
            console.log('hay lista: ', imagenes_add)
            const file = archivos[i]
            const reader = new FileReader();    
            const container = document.createElement('div');
            container.classList.add('imagen-container')
            const img = document.createElement('img');
            const trashIcono = document.createElement('i')
            trashIcono.classList.add('fas', 'fa-trash-alt', 'borrar-icon')

        trashIcono.addEventListener('click', function() {
            container.remove();
            eliminar_img.push(archivos[i])
            console.log('eliminando: ', eliminar_img)
        })

        reader.onload = function(e) {
            // convert image file to base64 string
            img.src = reader.result
            container.appendChild(img)
            container.appendChild(trashIcono)
            previsual.appendChild(container)
            previsual.style.display = 'block';
            imagenes_add.push(archivos[i])

            console.log('cargadas para enviar', imagenes_add)
            let dataTransfer = new DataTransfer()
            for (let file of imagenes_add) {
                dataTransfer.items.add(file)
            }
            imagenes_edit.files = dataTransfer.files
        }
        reader.readAsDataURL(archivos[i]);
        }
    })

    document.querySelector('.add-img-edit').addEventListener('click', function (event) {
            event.preventDefault();
            
            imagenes_edit.click()        
    });

    formularioEdicion.addEventListener('submit', function enviarForm(e) {
        const id = this.dataset.id;
        console.log('eliminadas: ', eliminar_img);
        let form = e.target                  
        let formData = new FormData(form);

        formData.append('imagenes_eliminadas', JSON.stringify(eliminar_img));

        fetch(`/foro/${modelo}/${id}/edit-foto`,  {
        method: 'POST',
        body: formData,
        headers: {
        "X-CSRFToken": getCSRFToken(),
        "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('imágenes actualizadas')
    })
    .catch(error=> {
        console.log('Error:', error)});   
});

function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

document.getElementById('add_url').addEventListener('click', function(e){
    e.preventDefault();
    let url_add =document.querySelector('.add_url');
    url_add.style.display = 'block';
});

document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input[type="url"]');

    inputs.forEach((input) =>{
        input.addEventListener('input', (event) => {
            const modelo = event.target.dataset.model
            let inputPrincipal = document.getElementById('url')
            let inputLink = document.getElementById('link-post')
            let prevLink = document.getElementById("link-prev-post")
            
        previsual.style.display = 'block';
        const url = inputPrincipal.value;
        const link = inputLink.value;
        prevLink.style.display = 'block'
        const linked = `<a href="${link}" target="_blank">${link}</a>`
        prevLink.innerHTML = linked

        if (!url) return;

        const container = document.createElement('div');
        container.classList.add('imagen-container')
        const img = document.createElement('img');
        img.src = url;

        const trashIcono = document.createElement('i')
        trashIcono.classList.add('fas', 'fa-trash-alt', 'borrar-icon')

        trashIcono.addEventListener('click', function() {
            container.remove();
            input.value = '';
            })
            container.appendChild(img)
            container.appendChild(trashIcono)
            previsual.appendChild(container)
            previsual.style.display = 'block';
            })
        })
    });

    document.addEventListener('DOMContentLoaded', () => {
        const inputs_file = document.querySelectorAll('input[type="file"]')

        inputs_file.forEach((input) =>{
            input.addEventListener('input', (event) => {
                const inputId = event.target.id     
                const dataId = event.target.dataset.id
                const modelo = event.target.dataset.model
                let inputAdjunto = null
                let prevFile = null
                const extensionesValidas =['.jpg', '.png', '.pdf', '.txt', '.zip', '.docx'];

                if(modelo === 'respuesta') {
                    inputAdjunto = document.getElementById('archivo')
                    prevFile = document.getElementById("file-prev-resp")
                }

            const archivos= inputAdjunto.files;
            Array.from(archivos).forEach((archivo) => {
                const extension = archivo.name.substring(archivo.name.lastIndexOf('.')).toLowerCase(); // Extrae .pdf, .jpg, etc.
                if (!extensionesValidas.includes(extension)) {
                    alert(`Extensión ${extension} no permitida. Solo se aceptan ${extensionesValidas.join(', ')}`)
                } else {
                    prevFile.style.display = 'block'
                    const container = document.createElement('div');
                    const icono = document.createElement('i');
                    // <a href="{{ archivo.archivo.url }}" download>{{ archivo.archivo.name|cut:"adjuntos/" }}</a>
                    if (extension == '.pdf') {
                        icono.classList.add('fas', 'fa-file-pdf')
                        icono.style.fontSize = '2rem'
                    } else if (extension === '.jpg' || extension === '.jpeg' || extension === '.png') {
                        icono.classList.add('fas', 'fa-file-image');
                        icono.style.fontSize = '2rem'
                    } else if (extension === '.txt') {
                        icono.classList.add('fas', 'fa-file-alt');
                        icono.style.fontSize = '2rem'
                    }else if (extension === '.docx') {
                        icono.classList.add('fas', 'fa-file-word')
                        icono.style.fontSize = '2rem'
                    }else if (extension === '.zip') {
                        icono.classList.add('fas', 'fa-file-zipper')
                        icono.style.fontSize = '2rem'
                    } else {
                        icono.classList.add('fas', 'fa-file');
                        icono.style.fontSize = '2rem'
                    }
                    let nombre_archivo = archivo.name
                    console.log('los adjuntos: ', archivo)
                    container.appendChild(icono)
                    prevFile.innerHTML = nombre_archivo
                    prevFile.appendChild(container);
                    }
                })
            })
        })
    });
