$(function () {

    $('.nav li').on({
            mouseenter: function () {
                       $(this).css({
                            'background-color': '#8adbd5'
                        });
            },
            mouseleave: function () {
                               $(this).removeAttr("style");
            }
    });

    $("#dropdown li a").on("click", function () {
        $("#pick").text(this.text);
        $('#hidGender').val(this.text);
    });

    $(document).on("click",'#dropdownUpd li a',function () {
        $("#pickUpd").text(this.text);
        $('#hidGenderUpd').val(this.text);
    });

    $('#frndModal #frnd-modal .sendReqClass').on('click', function () {
        var toFriend = {"toId":$(this).attr('id')};
        var btn = $(this).text();
        var url = "";
        if(btn == "Send Request")
        {
            $(this).text("Cancel Request");
            url = "/sendRequest";
        }
        else if(btn == "Unfriend")
        {
            url = "/unfriend";
            $(this).text("Send Request");
            $(this).closest('div').find('.frndClass').remove();
        }
        else{
            if(btn != "Deny")
            {
                $(this).text("Send Request");
                url = "cancelRequest"
            }
            else
            {
                $(this).closest('button').text('Send Request');
                $(this).remove()
                url ="/denyRequest";
            }
        }
        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify(toFriend),
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {
                console.log(result);
            }
        });
    });

    $('.acceptReqClass').on('click', function () {
        var toFriend = { "toId": $(this).attr('id') };
      //  $(this).closest('div').remove();
      $(this).parent().parent().remove();
        $.ajax({
            type: "POST",
            //url: "http://localhost:86/acceptRequest",
            //url: "{{url_for('acceptRequest')}}",
            url: "/acceptRequest",
            //data: toFriend,
            data: JSON.stringify(toFriend),
           // data: JSON.stringify($(this).attr('id'), null, '\t'),
           // data: { "toId": JSON.stringify($(this).attr('id')) },
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {
                console.log(result);
            }
        });
    });

    $('.like').on('click', function () {
        likeBtn = $(this).text();
        var url = "";
        var user_id = $('#hidUser').val();
        var data = { "post_id":$(this).attr('id'),"liked_by": user_id };
        if(likeBtn == 'Like')
        {
            $(this).text('Unlike');
            url = "/like";
        }
        else{
            $(this).text('Like');
            url = "/unlike";
        }
        $.ajax({
            type: "POST",
            url: url,
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {
                console.log(result);
            }
        });
    });

    $('.comment').on('click', function () {
        var user_id = $('#hidUser').val();
        var post_id = $(this).attr('id')
        var comment = $('#'+post_id+'comment').val();
        $('#'+post_id+'comment').val('');
        var data = { "post_id":post_id,"comment":comment,"comment_by":user_id  };
        var username = $('#hidUserName').val();
        var html = '<div class="row"><div class="col-md-2"><label class="label label-warning">'+username+'</label></div><div><p>'+comment+'</p></div></div>'
        $('#'+post_id+'newComment').append(html);
        $.ajax({
            type: "POST",
            url: "/comment",
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {
                console.log(result);
            }
        });
    });


    $('#testPost').click(function(){
        var testData = {"check":"Found"};
        $.ajax({
            type: "POST",
           // url: "http://localhost:86/testpost",
            url: "/testpost",
           // data: JSON.stringify(testData, null, '\t'),
           data: JSON.stringify(testData),
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {
                console.log(result);
            }
        });
    });

    $("#imgUpload").click(function () {        //To open a fileupload on image click
        $('#image_id').trigger('click');
        $('#showImage').css("border", "1px solid #dcd4d4");
        return false;
    }); //End

    $(".updImg").on('click',function () {        //To open a fileupload on image click
        var post_id = $(this).attr('id')
        $('#'+post_id+'image_id').trigger('click');
        $('#'+post_id+'showImg').css("border", "1px solid #dcd4d4");
        return false;
    }); //End

    $('.showAllCmt').on('click',function(){
       var post_id = $(this).attr('id');
       var imgDiv = $('#'+post_id+'imgDiv').html();
       $('#comment-body').append(imgDiv);
       $('#comment-body').find('img').css('width','40%');
       $('#comment-body').append($('#'+post_id+'hidComments').html());
       $('#comment-body #'+post_id+'hidComments').css('display','inline');
       //$('#'+post_id+'allCommentDiv hidComments').
       $('#commentModal').modal('show');
    });

    $('#commentModal .close').click(function(){
        $('#commentModal .modal-body div').html('');
    });

    $('#updateModal .close').click(function(){
        $('#updateModal .modal-body #update-body').html('');
    });

    $('#frndIcon').click(function(){
       $('#frndModal').modal('show');
       return false;
    });

    $('#viewMsg').click(function(){
        $.ajax({
                type: "POST",
                url: "/clearMsgCount",
                contentType: 'application/json;charset=UTF-8',
                success: function (result) {
                    console.log(result);
                }
        });
       $('#msgModal').modal('show');
       return false;
    });

    $('.updateIcon').on('click',function(){
        var post_id = $(this).attr('id');
        $('#update-body').append($('#'+post_id+'updateDiv').html());
        $('#update-body #'+post_id+'updateDiv').css('display','inline');
        $('#updateModal').modal('show');
        $('#update-body').removeAttr("style");
        return false;
    });


    function getUserInfo(ele){
        $('#update-body').html('');
        var user_id = $('#hidUser').val();
        var profile_id = $(ele).attr('id');
        var data = {"id":profile_id};
        var html = "";

            $.ajax({
                type: "POST",
                url: "/getUserInfo",
                data: JSON.stringify(data),
                contentType: 'application/json;charset=UTF-8',
                success: function (userInfo) {
                    if(userInfo.image == '' || userInfo.image == null)
                    {
                        userInfo.image = "img/user.jpeg";
                    }
                        if(user_id != profile_id)
                        {
                            html =  ` <div class="container col-md-12 col-sm-12 col-xs-12" id="otherUserInfoDiv">
                            <!-- style="height:100%;background-size:cover;background-image:url('/static/`+userInfo.image+`');" -->
                            <form method="POST" id="createForm" enctype="multipart/form-data">
                            <div class="form-group">
                                <div>
                                    <label class="form-contrl">Profile</label>
                                </div>
                                <div>
                                    <img id="showProPic" style="width:50%;" src="/static/`+userInfo.image+`"/>
                                </div>
                            </div>
                            <div class="form-group">
                                <div>
                                    <label class="form-contrl">Username</label>
                                </div>
                                <div>`
                                    +userInfo.uname+
                                `</div>
                            </div>
                            <div class="form-group">
                                <div>
                                    <label class="form-contrl">Country</label>
                                </div>
                                <div>`
                                    +userInfo.country+
                                `</div>
                            </div>
                            <div class="form-group">
                                <div>
                                    <label class="form-contrl">Date Of Birth</label>
                                </div>
                                <div>`
                                   +userInfo.dob+
                                `</div>
                            </div>
                            <div class="form-group">
                                <div>
                                    <label class="form-contrl">Gender</label>
                                </div>
                                <div>`
                                    +userInfo.gender+
                                `</div>
                            </div>
                            <div class="form-group">
                                <div>
                                    <label class="form-contrl">Email</label>
                                </div>
                                <div>`
                                    +userInfo.email+
                                `</div>
                            </div>
                            </form>
                            </div>`;
                        }
                        else
                        {
                            html = `
                            <div class="container col-md-12" id="userInfoDiv">
                            <form method="POST" id="updateUserInfo" enctype="multipart/form-data">
                                <div class="form-group">
                                    <div>
                                        <label class="form-contrl">Username</label>
                                    </div>
                                    <div>
                                        <input type="text" class="form-contrl" name="uname" value="`+userInfo.uname+`"/>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div>
                                        <label class="form-contrl">Country</label>
                                    </div>
                                    <div>
                                        <input type="text" class="form-contrl" value="`+userInfo.country+`" name="country" />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div>
                                        <label class="form-contrl">Date Of Birth</label>
                                    </div>
                                    <div>
                                        <input type="text" class="form-contrl" value="`+userInfo.dob+`" name="dob" />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div>
                                        <label class="form-contrl">Gender</label>
                                    </div>
                                    <div>
                                        <div class="dropdown">
                                                <button type="button" class="btn btn-success" id="pickUpd">`+userInfo.gender+`</button>
                                                <button type="button" class="btn btn-success" data-toggle="dropdown"><span class="caret"></span></button>
                                            <ul class="dropdown-menu updateDdl" id="dropdownUpd">
                                                <li><a href="#">Female</a></li>
                                                <li><a href="#">Male</a></li>
                                                <li><a href="#">Others</a></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div>
                                        <label class="form-contrl">Email</label>
                                    </div>
                                    <div>
                                        <input type="text" class="form-contrl" value="`+userInfo.email+`" name="email" />
                                        <input type="hidden" name="gender" id="hidGenderUpd" value="`+userInfo.gender+`"/>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div>
                                        <label class="form-contrl">Upload Image</label>
                                    </div>
                                    <div class="">
                                        <img id="update_pro_pic" style="width:50%" src="/static/`+userInfo.image+`">
                                        <input type="file" class="form-contrl" name="image" onchange="loadProPicUpdate(event)"/>
                                        <input type="hidden" name="imageOld" value="`+userInfo.image+`">
                                    </div>
                                </div>
                                <div>
                                    <input type="submit" class="form-contrl btn-success" name="create" value="Update Info"/>
                                </div>
                            </form>
                            </div>
                            `;
                        }
                    $('#update-body').append(html);
                    $('#update-body').css("height","80%");
                    $('#updateModal').modal('show');

                }
            });
    }

    $('.userProfile').click(function(){
            getUserInfo(this);
            return false;
    });

    $('.propicDiv').on('click',function(){
        getUserInfo(this);
        return false;
    });

    $('.msgIcon').on('click',function(){
        $('#update-body').html('');
        var toUserId = $(this).attr('id');
        $('#hidToUser').val(toUserId);
         var uname = $('#hidUserName').val();
        msgUserName = $($(this).closest('div')).prev().find('label').text();
        $('#updTitle').html(msgUserName);
        $('#update-body').append($('#showMsgDiv').html());
        $('#update-body #showMsgDiv').css("display","inline");
        $('#update-body').css("height","");
        $('#frndModal').modal('hide');
        $('#updateModal').modal('show');
    });

        $(document).on('click','.sendMsg',function () {
        var uname = $('#hidUserName').val();
        var toUserId = $('#hidToUser').val();
        var msg = $('#msgTxt').val();
        $('#msgTxt').val('');
        var data = { "toId":toUserId,"msg":msg  };
        var html = '<div class="col-md-offset-6"><label class="label label-primary">'+uname+'</label><p class="">'+msg+'</p></div>'
        $('#update-body .sentMsg').append(html);
        $.ajax({
            type: "POST",
            url: "/msg",
            data: JSON.stringify(data),
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {
                console.log(result);
            }
        });
    });


    $(".msgP").on({
    mouseenter: function () {
               $(this).css({
                    'padding': '1%',
                    'border': '1px solid #dacdcd',
                    'background-color': '#2db3ab4a'
                });
    },
    mouseleave: function () {
                       $(this).removeAttr("style");
    }
    });

    $(document).on('click','.viewMsgDiv',function(){
         $('#update-body').html('');
        var uname = $($(this).find('p')).attr('id');
        var toUserId = $(this).attr('id');
        var fromUserId = $('#hidUser').val();
        var data = {"id":toUserId};
            $.ajax({
                type: "POST",
                url: "/showMsgs",
                data: JSON.stringify(data),
                contentType: 'application/json;charset=UTF-8',
                success: function (msgs) {
                    var html = "";

                    for(var i=0;i<msgs.length;i++)
                    {
                        if(fromUserId == msgs[i].id)
                           html += '<div class="col-md-offset-6"><label class="label label-primary">'+msgs[i].uname+'</label><p class="">'+msgs[i].msg+'</p></div>';
                        else
                           html += '<div><label class="label label-primary">'+msgs[i].uname+'</label><p class="">'+msgs[i].msg+'</p></div>';
                    }
                    $('#showMsgDiv .sentMsg').append(html);
                     html = $('#showMsgDiv').html();
                    //html += '<div id="sentMsg"></div><textarea id="msgTxt"></textarea><button class="sendMsg">Send</button>';
                     $('#hidToUser').val(toUserId);
                     $('#msgModal').modal('hide');
                     $('#updTitle').html(uname);
                     $('#update-body').append(html);
                    $('#update-body #sentMsg').css({"display":"inline",'overflow-y':'scroll','height':'40%'});
                     $('#updateModal').modal('show');
                }
        });
    });


    $('.notLogged').click(function(){
                $.ajax({
                type: "POST",
                url: "/notLogged",
                contentType: 'application/json;charset=UTF-8',
                success: function (result) {
                    console.log(result);
                }
        });
    });

});


//Load file from fileUpload to Img
var loadFile = function (event) {
    var output = document.getElementById("showImage");
    output.src = window.URL.createObjectURL(event.target.files[0]);
};

//Load file from fileUpload to Img
var loadUpdateImg = function (event) {
   var output = document.getElementById(event.target.id+"showImg");
    output.src = window.URL.createObjectURL(event.target.files[0]);
};

var loadProPic = function (event) {
   var output = document.getElementById('showProPic');
    output.src = window.URL.createObjectURL(event.target.files[0]);
};

var loadProPicUpdate = function (event) {
   var output = document.getElementById('update_pro_pic');
    output.src = window.URL.createObjectURL(event.target.files[0]);
};