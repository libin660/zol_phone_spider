<?php
/**
 * 设置头部让网页能正常显示中文名字
 */
header("content-type:application/json;charset=utf-8");
date_default_timezone_set("Asia/Shanghai");
echo '<meta http-equiv="content-type" content="text/html;charset=utf-8">';

/**
 * 递归一个文件夹下的所有子文件夹和文件
 */
function my_dir($dir) {
    $files = array();
    if(@$handle = opendir($dir)) {
        while(($file = readdir($handle)) !== false) {
            if($file != ".." && $file != ".") {
                if(is_dir($dir."/".$file)) {
                    $files[$file] = my_dir($dir."/".$file);
                } else {
                    $files[] = $file;
                }
            }
        }
        closedir($handle);
        return $files;
    }
    return false;
}

/**
 * 查询数据库分页获取旧版图片链接
 */
$c = mysqli_connect("127.0.0.1","root",'root',"zol");
mysqli_query($c,"set names utf-8");

$list = mysqli_query($c,
" SELECT id,fullname FROM `cell_phone` order by id asc limit 16000,2000 ");

/**
 * 旧版存放地址
 */
$dir = "F:/zol/000001-100000/";
$newdir = "F:/NewZol/9/";
$extarr = ['.jpg','.jpeg','.png','.gif','.bmp'];

/**
 * 循环每条记录进行处理
 */
while($row = $list->fetch_assoc() ){

    $tmpdir = $dir.$row['id'];
    $files = my_dir($tmpdir);
    // print_r($files);
    //if($row['aliasname'] != "") {
       // $name = $row['aliasname'];
    //}else{

    /**
     * 处理不能用于文件名的特殊符号
     */
    $row['fullname'] = str_replace("(","",$row['fullname']);
    $row['fullname'] = str_replace(")","",$row['fullname']);
    $row['fullname'] = str_replace("（","",$row['fullname']);
    $row['fullname'] = str_replace("）","",$row['fullname']);
    $row['fullname'] = str_replace("/","",$row['fullname']);
    $row['fullname'] = str_replace(":","",$row['fullname']);
    $name = $row['fullname'];
    //}

    /**
     * appearance的处理
     */
    if(isset($files['product_appearance']) &&
        count($files['product_appearance']) != 0){
        foreach ($files['product_appearance'] as $k1 => $appearance){
            $t1 = explode(".",$appearance);
            $ext = ".".end($t1);
            if(!in_array($ext,$extarr)){
                echo $ext;echo "\r\n\r\n";
            }else{
                $oldpath = $tmpdir.'/product_appearance/'.$appearance;
                // echo "\r\n\r\n";
                $newpath = $newdir.$row['id']."-[".$name."]-appearance-".($k1+1).$ext;
                $newpath = iconv('UTF-8', 'GB2312', $newpath);
                $aa = copy($oldpath,$newpath);
                if($aa == false){
                    echo "***********************";
                    echo $oldpath;
                    echo "\r\n\r\n";
                    echo $newpath;
                }
            }
        }
    }


    /**
     * introduce的处理
     */
    if(isset($files['product_introduce']) &&
        count($files['product_introduce']) != 0){
        foreach ($files['product_introduce'] as $k1 => $appearance){
            $t1 = explode(".",$appearance);
            $ext = ".".end($t1);
            if(!in_array($ext,$extarr)){
                echo $ext;echo "\r\n\r\n";
            }else {
                $oldpath = $tmpdir . '/product_introduce/' . $appearance;
                // echo "\r\n\r\n";
                $newpath = $newdir . $row['id'] . "-[" . $name . "]-introduce-" . ($k1 + 1) . $ext;
                $newpath = iconv('UTF-8', 'GB2312', $newpath);
                $aa = copy($oldpath, $newpath);
                if ($aa == false) {
                    echo "***********************";
                    echo $oldpath;
                    echo "\r\n\r\n";
                    echo $newpath;
                }
            }
        }
    }


    /**
     * logo的处理
     */
    if(isset($files['product_logo']) && count($files['product_logo']) != 0){
        $logo = $files['product_logo'][0];
        $t1 = explode(".",$logo);
        $ext = ".".end($t1);
        $oldpath = $tmpdir.'/product_logo/'.$logo;
        // echo "\r\n\r\n";
        if(!in_array($ext,$extarr)){
            echo $ext;echo "\r\n\r\n";
        }else {
            $newpath = $newdir . $row['id'] . "-[" . $name . "]-logo" . $ext;
            $newpath = iconv('UTF-8', 'GB2312', $newpath);
            $aa = copy($oldpath, $newpath);
            if ($aa == false) {
                echo "***********************";
                echo $oldpath;
                echo "\r\n\r\n";
                echo $newpath;
            }
        }
    }

    // var_dump($row['id']);
    // die;

} // while row




