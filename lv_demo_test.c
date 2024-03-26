
//图片数量，有几个图片写几个，即my_img长度
#define IMAGE_ICON_NUM  147
//每行几个图片
#define IMAGE_ROW_NUM   7
//图片尺寸
#define IMAGE_SIZE      100
//图片偏移（未用到）
#define IMAGE_OFFSET_X  0
#define IMAGE_OFFSET_Y  0
//图片缩放比例
#define IMAGE_SCALE     0.4f

//图片对象
lv_obj_t * image[IMAGE_ICON_NUM];
//初始坐标（程序自动根据以上参数计算）
lv_point_t init_pos[IMAGE_ICON_NUM];
//拖拽位置
lv_point_t point_final = {0,0};

LV_IMAGE_DECLARE(img_picture_1_dsc);
LV_IMAGE_DECLARE(img_picture_2_dsc);
LV_IMAGE_DECLARE(img_picture_3_dsc);
LV_IMAGE_DECLARE(img_picture_4_dsc);
LV_IMAGE_DECLARE(img_picture_5_dsc);
LV_IMAGE_DECLARE(img_picture_6_dsc);
LV_IMAGE_DECLARE(img_picture_7_dsc);
LV_IMAGE_DECLARE(img_picture_8_dsc);
LV_IMAGE_DECLARE(img_picture_9_dsc);
LV_IMAGE_DECLARE(img_picture_10_dsc);

// 声明lv_img_dsc_t类型的数组my_img
const lv_img_dsc_t * my_img[] = {
    &img_picture_1_dsc,
    &img_picture_2_dsc,
    &img_picture_3_dsc,
    &img_picture_4_dsc,
    &img_picture_5_dsc,
    &img_picture_6_dsc,
    &img_picture_7_dsc,
    &img_picture_8_dsc,
    &img_picture_9_dsc,
    &img_picture_10_dsc,
};

static void img_drag_event_handler(lv_event_t * e)
{
    int i;
    lv_sqrt_res_t lenth;
    int w = lv_obj_get_width(lv_screen_active());
    int h = lv_obj_get_height(lv_screen_active());
    lv_obj_t * obj = lv_event_get_target(e);
    lv_indev_t * indev = lv_indev_active();
    if(indev == NULL)  return;

    lv_point_t vect;
    lv_indev_get_vect(indev, &vect);

    point_final.x += vect.x;
    point_final.y += vect.y;

    for(i = 0;i < IMAGE_ICON_NUM;i++)
    {
        int pos_x,pos_y;
        pos_x = init_pos[i].x + point_final.x;
        pos_y = init_pos[i].y + point_final.y;
        //计算图片距离屏幕中心距
        lv_sqrt((pos_x - w / 2) * (pos_x - w / 2) + \
                (pos_y - h / 2) * (pos_y - h / 2), \
                &lenth, 0xFFFF);
        if(1)//根据距离屏幕中心距离确定缩放大小
        {
            lv_obj_set_style_transform_scale(image[i],(400 - lenth.i) * IMAGE_SCALE,_LV_STYLE_STATE_CMP_SAME);
            lv_obj_set_pos(image[i], pos_x - (400 - lenth.i) * 0.1, pos_y - (400 - lenth.i) * 0.1);
        }
        else //一般大
        {
            lv_obj_set_pos(image[i], pos_x , pos_y);
        }
    }
}

void lv_demo_test(void)
{
    int i;
    int offset_x,offset_y;
    lv_obj_t * parent = lv_screen_active();
    lv_obj_set_scrollbar_mode(parent,LV_SCROLLBAR_MODE_OFF);
    lv_obj_set_scroll_dir(parent,LV_DIR_NONE);

    offset_x = IMAGE_OFFSET_X;
    offset_y = IMAGE_OFFSET_Y;
    //初始化初始位置摆列
    for(i=0;i<IMAGE_ICON_NUM;i++)
    {
        int x,y,l,w,h;
        lv_sqrt_res_t len;
        w = lv_obj_get_width(parent);
        h = lv_obj_get_height(parent);
        image[i] = lv_image_create(parent);
        image[i]->user_data = i;
        lv_image_set_src(image[i],my_img[i]);
        if((i / IMAGE_ROW_NUM) % 2){
            x = (i % IMAGE_ROW_NUM) * IMAGE_SIZE + IMAGE_SIZE / 2 + offset_x;
        }
        else {
            x = (i % IMAGE_ROW_NUM) * IMAGE_SIZE + offset_x;
        }
        y = (i / IMAGE_ROW_NUM) * IMAGE_SIZE * 0.886f + offset_y;
        lv_sqrt((x - w / 2) * (x - w / 2) + (y - h / 2) * (y - h / 2), &len, 0xFFFF);
        if(1)
        {
            lv_obj_set_style_transform_scale(image[i],(w / 2 - len.i) * IMAGE_SCALE,_LV_STYLE_STATE_CMP_SAME);
        }
        else
        {
            lv_obj_set_style_transform_scale(image[i],128,_LV_STYLE_STATE_CMP_SAME);
        }
        lv_obj_set_x(image[i], x);
        lv_obj_set_y(image[i], y);
        init_pos[i].x = x;
        init_pos[i].y = y;
        lv_obj_add_flag(image[i],LV_OBJ_FLAG_IGNORE_LAYOUT);
        lv_obj_add_flag(image[i],LV_OBJ_FLAG_CLICKABLE);
        lv_obj_add_event_cb(image[i],img_drag_event_handler, LV_EVENT_PRESSING, NULL);
    }
}
