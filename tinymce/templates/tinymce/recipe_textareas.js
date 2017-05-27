/**
 * Created by Admin on 5/27/2017.
 */
tinyMCE.init({
    mode: "textareas",
    theme: "advanced",
    plugins: "directionality,paste,searchreplace",
    language: "{{ language }}",
    directionality: "{{ directionality }}",
});