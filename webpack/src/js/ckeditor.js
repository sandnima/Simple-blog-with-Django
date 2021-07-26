// Below plugins added to custom build
// Alignment
// TextPartLanguage
// WordCount
// AutoSave
// Markdown

import ClassicEditor from '../../ckeditor5-build-modern-blog/build/ckeditor';

const minWords = 300;
const wordsBox = document.querySelector( '.words' );

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
        },
        wordCount: {
            onUpdate: stats => {
                console.log( `Characters: ${ stats.characters }\nWords: ${ stats.words }` );
                const isOverMinimum = stats.words > minWords;

                if (stats.words <= 1) {
                    wordsBox.textContent = `${ stats.words } word`;
                }
                else {
                    wordsBox.textContent = `${ stats.words } words`;
                }
                wordsBox.classList.toggle( 'text-success', isOverMinimum );
            }
        },
    })
    // .then( editor =>{
    //     const wordCountPlugin = editor.plugins.get( 'WordCount' );
    //     const wordCountWrapper = document.getElementById( 'word-count' );
    //
    //     wordCountWrapper.appendChild( wordCountPlugin.wordCountContainer );
    // })
    .catch( error => {
        console.error( error );
    });

