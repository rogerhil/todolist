jQuery(function($) {
    ajaxSubmit($('form[todo-add]'), function (data) {
        if (!data.success) {
            $('form[todo-add]').html(data.content);
            $('.datetimepicker').datetimepicker({language: 'pt-BR'});
        }
    });
    $('.datetimepicker').datetimepicker({language: 'pt-BR'});
    initTable();
});

function ajaxSubmit($el, callback) {
    $el.unbind('submit').on('submit', function(event) {
        var $form = $(this);
        var $target = $($form.attr('data-target'));
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize(),
            success: function(data, status) {
                if (data.success) {
                    $target.html(data.content);
                    initTable();
                    $target.find('td').effect('highlight', 1000);
                } else {
                    if (!callback) {
                        alert(data.errors);
                    }
                }
                if (callback) {
                    callback(data);
                }
            },
            error: function (data) {
                alert('Status: ' + data.status + ' ' + data.statusText);
            }
        });
        event.preventDefault();
    });
}

function initTable() {
    ajaxSubmit($('form[delete-form]'));
    ajaxSubmit($('form[mark-done-form]'));
    ajaxSubmit($('form[change-priority-form]'));
    ajaxSubmit($('form[change-due-date-form]'));
    ajaxSubmit($('form[change-description-form]'));
    $('.description').unbind('click').click(changeDescription);
    $('.due-date').unbind('click').click(changeDueDate);
    $('button.change-priority').unbind('click').click(changePriority);
    $('button.delete').unbind('click').click(deleteTodo);
    $('button.mark-done').unbind('click').click(markAsDone);
    $('.datetimepicker-change').datetimepicker({language: 'pt-BR'});
    sorting();
}

function sorting() {
    $('th.sorting').unbind('click').click(function () {
        var $self = $(this);
        var orderby = $('table.table').attr('orderby');
        var url = $('table.table').attr('url');
        var sorting = $self.attr('sorting');
        if ($self.hasClass('sorting_desc')) {
            sorting = '-' + sorting;
        }
        var data = get_query_string_params();
        data.order = sorting;
        $.ajax({
            url: url,
            data: data,
            success: function(data, status) {
                if (data.success) {
                    $('#listing').html(data.content);
                    initTable();
                    $('#listing').find('td').effect('highlight', 1000);
                } else {
                    alert(data.errors);
                }
            }
        });
    });
}


function deleteTodo(e) {
    if (!confirm("Are you sure you want to delete this item?")) return;
    $(this).parent().find('form[delete-form]').trigger('submit');
}

function markAsDone(e) {
    $(this).parent().find('form[mark-done-form]').trigger('submit');
}

function changePriority(e) {
    var $form = $(this).parent().find('form[change-priority-form]');
    var pos = $(this).position();
    var $menu = $("#priority_menu");
    $menu.css('top', (pos.top - 30) + 'px');
    $menu.css('left', (pos.left - 150) + 'px');
    $menu.modal();
    $menu.find("button").unbind('click').click(function () {
        var priority = $(this).attr("value");
        $form.find('input[name=priority]').val(priority);
        $form.trigger('submit');
        $menu.modal('hide');
    });
}

function changeDueDate(e) {
    closeOthers();
    var $form = $(this).find('form[change-due-date-form]');
    var $text = $(this).find('span');
    var $field = $form.find('input[name=due-date]');
    if (!$field.is(':visible')) {
        $form.fadeIn();
        $text.hide();
        $field.focus();
        $field.select();
    }
    $form.find("button[type=submit]").unbind('click').click(function () {
        $form.hide();
        $text.fadeIn();
    });
}

function closeOthers(fname) {
    $('form[change-description-form]').hide();
    $('form[change-description-form]').parent().find('span').show();
    $('form[change-due-date-form]').hide();
    $('form[change-due-date-form]').parent().find('span').show();
}

function changeDescription(e) {
    closeOthers();
    var $form = $(this).find('form[change-description-form]');
    var $text = $(this).find('span');
    var $field = $form.find('input[name=description]');
    if (!$field.is(':visible')) {
        $form.fadeIn();
        $text.hide();
        $field.focus();
        $field.select();
    }
    $form.find("button[type=submit]").unbind('click').click(function () {
        $form.hide();
        $text.fadeIn();
    });
}