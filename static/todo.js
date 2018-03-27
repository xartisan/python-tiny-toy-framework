/**
 * convert timestamp to local time string
 * @param timestamp
 * @returns {string}
 */
function stringifyTime(timestamp) {
    var dt = new Date(timestamp * 1000);
    return dt.toLocaleDateString();
}

/**
 * convert todo to html
 * @param todo
 */
function todoTemplate(todo) {
    var id = todo.id;
    var title = todo['task'];
    var ut = todo.updated_time;
    var t = `
        <div class="todo-cell" id='todo-${id}' data-id="${id}">
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">删除</button>
            <span class='todo-title'>${title}</span>
            <time class='todo-ut'>${ut}</time>
        </div>
    `
    return t;
}

/**
 * insert todo to todolist
 * @param todo
 */
function insertTodo(todo) {
    var t = todoTemplate(todo);
    var todoList = elem('.todo-list');
    todoList.insertAdjacentHTML('beforeend', t);
}

/**
 * load todo list
 */
function loadTodoList() {
    ajaxGet('api/todo/all', function (r) {
        var todoList = JSON.parse(r);
        for (var i = 0; i < todoList.length; i++) {
            insertTodo(todoList[i]);
        }
    })
}

/**
 *
 */
function bindEventTodoAdd() {
    var b = elem('#id-button-add');
    b.addEventListener('click', function (e) {
        var input = elem('#id-input-todo');
        var task = input.value;
        var form = {
            'task': task,
        };
        ajaxPost('api/todo/add', form, function (r) {
            var todo = JSON.parse(r);
            insertTodo(todo);
        });
    })
}

function bindEventTodoDelete() {
   var todoList = elem('.todo-list');
   todoList.addEventListener('click', function (e) {
       var t = e.target;
       if t.classList.contains('')
   })
}