var token_key = 'uuid'
token = $.cookie(token_key)
if(token === undefined){
    alert(token)
    if(!window.location.href.includes('/desktop/login')){
        alert('请登录')
        parent.window.location.href = '/desktop/login'
    }
}
if(!window.location.href.includes('/desktop/login')){
    $.ajaxSetup({
        beforeSend:function(xhr){
            xhr.setRequestHeader('Authorization', 'Token '+$.cookie(token_key))
        }
    })
}
//登录模块
function to_login(){
    submit_data = {}
    submit_data['username'] = $("input").eq(0).val()
    submit_data['password'] = $('input').eq(1).val()
    token = $.cookie('token')
    // if(typeof token === "undefined" || token === null){
    //   alert('请登录')
    // }
    // else{
    //   alert('已经登录')
    //   alert(token)
    // }
    $.ajax({
      url:'/userauth/login/',
      method:'POST',
      data:submit_data,
      async:true,
      success:function(data){
        alert('登录成功')
        if('access' in data){
          $.cookie('access', data['access'])
          $.cookie('refresh', data['refresh'])
        }else if('uuid' in data){
          $.cookie('uuid', data['uuid'], {expires:7, path:'/'})
          alert(data['uuid'])
        }
        window.location.href = '/'
      },
      error:function(err){
        data = err.responseJSON
        if('username' in data){
          alert(data['username'])
        }
      }
    })
  }
  $('#to_login').eq(0).click(function(){to_login()})
  function to_register(){
    submit_data = {}
    input_label = $("form").eq(0).find("input")
    submit_data['username'] = input_label.eq(0).val()
    submit_data['email'] = input_label.eq(1).val()
    submit_data['password'] = input_label.eq(2).val()
    submit_data['password_again'] = input_label.eq(3).val()
    alert(submit_data['username'])
    $.ajax({
      url:'/userauth/user/',
      method:'POST',
      data:submit_data,
      async:true,
      success:function(){
        alert('添加成功')
      },
      error:function(data){
        err = data.responseJSON
        alert(err['username'])
      }
    })
  }
  $('#to_register').eq(0).bind('click', to_register)

  // linkmart 门店模块
  function get_store(){
    $.ajax({
      url:'/store/',
      method:'GET',
      async:true,
      success:function(data){
        selected = $('#register_store_id')
        $.each(data['results'], function(key, value){
            selected.append('<option value="'+value['id']+'">'+value['name']+'</option>')
        })
      },
      error:function(data){
        err = data.responseJSON
        alert(err)
      }
    })
  }

  function get_users(){
    $.ajax({
        url:'/userauth/user/',
        method:'GET',
        async:true,
        success:function(data){
            tr = $('#user_list tbody tr td')
            $.each(data['results'], function(key, val){
                h = $("<tr></tr>")
                new_tr = tr.clone()
                new_tr.eq(0).text(val['nid'])
                new_tr.eq(1).text(val['username'])
                new_tr.eq(2).html('<span class="badge badge-success">'+val['store_id']+'</span>')
                h.append(new_tr)
                $("#user_list tbody").append(h)
            })
            tr.hide()
        },
        error:function(data){
          err = data.responseJSON
          alert(err)
        }
      })
  }