import ClassicEditor from '../../ckeditor5-build-modern-blog/build/ckeditor';

ClassicEditor
    .create( document.querySelector( '#editor' ), {
        toolbar: {
            items: [
                'heading', '|',
                'bold', 'italic', 'link', 'undo', 'redo', 'alignment', 'bulletedList', 'numberedList', 'blockQuote',
            ],
            shouldNotGroupWhenFull: true
        },
        language: {
            // The UI will be English.
            ui: 'en',
            // But the content will be edited in Arabic.
            content: 'fa'
        }
    } )
    .catch( error => {
        console.error( error );
    } );
