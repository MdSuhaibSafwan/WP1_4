from django.db import models

##NEEDED LATER FOR POLYGON FIELDS##
#from django.contrib.gis.db import models
#from django.utils.translation import gettext_lazy as translate

class Addr(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    fromhn = models.CharField(max_length=12, blank=True, null=True)
    tohn = models.CharField(max_length=12, blank=True, null=True)
    side = models.CharField(max_length=1, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    plus4 = models.CharField(max_length=4, blank=True, null=True)
    fromtyp = models.CharField(max_length=1, blank=True, null=True)
    totyp = models.CharField(max_length=1, blank=True, null=True)
    fromarmid = models.IntegerField(blank=True, null=True)
    toarmid = models.IntegerField(blank=True, null=True)
    arid = models.CharField(max_length=22, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addr'


class Addrfeat(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    statefp = models.CharField(max_length=2)
    aridl = models.CharField(max_length=22, blank=True, null=True)
    aridr = models.CharField(max_length=22, blank=True, null=True)
    linearid = models.CharField(max_length=22, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    lfromhn = models.CharField(max_length=12, blank=True, null=True)
    ltohn = models.CharField(max_length=12, blank=True, null=True)
    rfromhn = models.CharField(max_length=12, blank=True, null=True)
    rtohn = models.CharField(max_length=12, blank=True, null=True)
    zipl = models.CharField(max_length=5, blank=True, null=True)
    zipr = models.CharField(max_length=5, blank=True, null=True)
    edge_mtfcc = models.CharField(max_length=5, blank=True, null=True)
    parityl = models.CharField(max_length=1, blank=True, null=True)
    parityr = models.CharField(max_length=1, blank=True, null=True)
    plus4l = models.CharField(max_length=4, blank=True, null=True)
    plus4r = models.CharField(max_length=4, blank=True, null=True)
    lfromtyp = models.CharField(max_length=1, blank=True, null=True)
    ltotyp = models.CharField(max_length=1, blank=True, null=True)
    rfromtyp = models.CharField(max_length=1, blank=True, null=True)
    rtotyp = models.CharField(max_length=1, blank=True, null=True)
    offsetl = models.CharField(max_length=1, blank=True, null=True)
    offsetr = models.CharField(max_length=1, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'addrfeat'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bg(models.Model):
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce = models.CharField(max_length=1, blank=True, null=True)
    bg_id = models.CharField(primary_key=True, max_length=12)
    namelsad = models.CharField(max_length=13, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'bg'
        db_table_comment = 'block groups'


class CommonAsyncrequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    date_responded = models.DateTimeField(blank=True, null=True)
    receiver = models.CharField(max_length=200)
    uuid = models.UUIDField()
    request_message = models.JSONField(blank=True, null=True)
    request_response = models.JSONField(blank=True, null=True)
    async_response = models.JSONField(blank=True, null=True)
    state = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'common_asyncrequest'


class CommonBin(models.Model):
    id = models.BigAutoField(primary_key=True)
    bin_id = models.SmallIntegerField(unique=True)
    max_filling = models.SmallIntegerField()
    reserved_plytype = models.OneToOneField('CommonPlytype', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_bin'


class CommonBinfilling(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    bin = models.ForeignKey(CommonBin, models.DO_NOTHING)
    ply = models.OneToOneField('CommonPly', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_binfilling'


class CommonBuffer(models.Model):
    id = models.BigAutoField(primary_key=True)
    tray_order = models.TextField()  # This field type is a guess.
    out_of_buffer = models.IntegerField(blank=True, null=True)
    end_effector = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50)
    priority_num = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'common_buffer'


class CommonCommandlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    date_processed = models.DateTimeField()
    direction = models.CharField(max_length=250)
    command = models.CharField(max_length=250)
    payload = models.JSONField(blank=True, null=True)
    success = models.BooleanField()
    result = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_commandlog'


class CommonConveyorarea(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    x_start = models.FloatField()
    x_end = models.FloatField()

    class Meta:
        managed = False
        db_table = 'common_conveyorarea'


class CommonConveyorareafilling(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    last_seen_encoder_value = models.IntegerField()
    x = models.FloatField()
    y = models.FloatField()
    alpha = models.FloatField()
    conveyor_area = models.ForeignKey(CommonConveyorarea, models.DO_NOTHING)
    ply = models.OneToOneField('CommonPly', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_conveyorareafilling'


class CommonCutter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    priority_num = models.IntegerField(unique=True)
    active_nest = models.ForeignKey('CommonNest', models.DO_NOTHING, blank=True, null=True)
    loaded_roll = models.ForeignKey('CommonRoll', models.DO_NOTHING, blank=True, null=True)
    offload_ready = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'common_cutter'


class CommonEndeffector(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    date_created = models.DateTimeField()
    end_effector_id = models.IntegerField(unique=True)
    shape = models.TextField()  # This field type is a guess.
    tcp = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'common_endeffector'


class CommonEndeffectorAllowedProcesses(models.Model):
    id = models.BigAutoField(primary_key=True)
    endeffector = models.ForeignKey(CommonEndeffector, models.DO_NOTHING)
    process = models.ForeignKey('CommonProcess', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_endeffector_allowed_processes'
        unique_together = (('endeffector', 'process'),)


class CommonEnvironment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    data = models.JSONField(blank=True, null=True)
    active_buffer = models.ForeignKey(CommonBuffer, models.DO_NOTHING, blank=True, null=True)
    active_end_effector = models.ForeignKey(CommonEndeffector, models.DO_NOTHING, blank=True, null=True)
    active_workorder = models.ForeignKey('CommonWorkorder', models.DO_NOTHING, blank=True, null=True)
    active_welding_table = models.ForeignKey('CommonWeldingtable', models.DO_NOTHING, blank=True, null=True)
    active_cutter = models.ForeignKey(CommonCutter, models.DO_NOTHING, blank=True, null=True)
    plc_mode = models.CharField(max_length=200, blank=True, null=True)
    conveyor_state = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'common_environment'


class CommonEventlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_fields = models.JSONField(blank=True, null=True)
    content_type = models.OneToOneField('DjangoContentType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_eventlist'


class CommonMaterial(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    material_id = models.CharField(max_length=200)
    coloured_thread_side = models.IntegerField()
    rev = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    thickness = models.FloatField()
    density = models.FloatField(blank=True, null=True)
    stiffness0 = models.FloatField()
    stiffness45 = models.FloatField(blank=True, null=True)
    stiffness90 = models.FloatField(blank=True, null=True)
    hold_distance0 = models.FloatField()
    hold_distance45 = models.FloatField(blank=True, null=True)
    hold_distance90 = models.FloatField(blank=True, null=True)
    backer_color_check = models.BooleanField()
    excess_backer_top = models.FloatField()
    excess_backer_bottom = models.FloatField()
    vacuum_perc = models.FloatField()
    vacuum_radius_min = models.FloatField()
    vacuum_radius_max = models.FloatField()
    cup_activation_time = models.FloatField()
    cup_deactivation_time = models.FloatField()
    ply_lift_speed = models.FloatField()
    ply_lift_accel = models.FloatField()
    robot_speed = models.FloatField()
    robot_accel = models.FloatField()
    buffer_speed = models.FloatField()
    buffer_accel = models.FloatField()
    fiber_dir_type = models.IntegerField()
    max_sagging_bridge = models.FloatField(blank=True, null=True)
    stiffness_angle = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_material'
        unique_together = (('material_id', 'rev'),)


class CommonNest(models.Model):
    id = models.BigAutoField(primary_key=True)
    sequence_num = models.IntegerField()
    state = models.CharField(max_length=20)
    material = models.ForeignKey(CommonMaterial, models.DO_NOTHING, blank=True, null=True)
    nest_file = models.ForeignKey('CommonNestfile', models.DO_NOTHING, blank=True, null=True)
    workorder = models.ForeignKey('CommonWorkorder', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_nest'


class CommonNestfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    nest_file = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'common_nestfile'


class CommonOffloadarea(models.Model):
    id = models.BigAutoField(primary_key=True)
    offload_area_id = models.IntegerField(unique=True)
    x_start = models.FloatField()
    x_end = models.FloatField()
    cutter = models.ForeignKey(CommonCutter, models.DO_NOTHING, blank=True, null=True)
    ply_supply = models.ForeignKey('CommonPlysupply', models.DO_NOTHING, blank=True, null=True)
    conveyor_area = models.OneToOneField(CommonConveyorarea, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_offloadarea'


class CommonOffloadareafilling(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    insert_x = models.FloatField()
    insert_y = models.FloatField()
    offload_area = models.ForeignKey(CommonOffloadarea, models.DO_NOTHING)
    ply = models.OneToOneField('CommonPly', models.DO_NOTHING)
    sequence_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'common_offloadareafilling'


class CommonPickinstruction(models.Model):
    id = models.BigAutoField(primary_key=True)
    pose_x = models.FloatField()
    pose_y = models.FloatField()
    pose_a = models.FloatField()
    ee_active_suction_cup_ids = models.TextField()  # This field type is a guess.
    ee_active_edge_cup_ids = models.TextField()  # This field type is a guess.
    ee_active_sensor_ids = models.TextField()  # This field type is a guess.
    offload_area = models.ForeignKey(CommonOffloadarea, models.DO_NOTHING, blank=True, null=True)
    data = models.JSONField()
    pose_z = models.FloatField()

    class Meta:
        managed = False
        db_table = 'common_pickinstruction'


class CommonPly(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    #shape = models.PolygonField(
    #    srid=28992,
    #    default=None,
    #    null=True,
    #    blank=True,
    #    help_text=translate("polygon of ply as in the nest (inserted with the right x,y,angle)"),
    #)  
    shape = models.TextField()  # This field type is a guess.
    insert_dxf_x = models.FloatField()
    insert_dxf_y = models.FloatField()
    date_cut = models.DateTimeField(blank=True, null=True)
    state = models.CharField(unique=True, max_length=20)
    data = models.JSONField()
    nest = models.ForeignKey(CommonNest, models.DO_NOTHING, blank=True, null=True)
    pick_instruction = models.ForeignKey(CommonPickinstruction, models.DO_NOTHING, blank=True, null=True)
    plytype = models.ForeignKey('CommonPlytype', models.DO_NOTHING, blank=True, null=True)
    roll = models.ForeignKey('CommonRoll', models.DO_NOTHING, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    ply_supply_offload_area = models.ForeignKey(CommonOffloadarea, models.DO_NOTHING, blank=True, null=True)
    external_id = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_ply'


class CommonPlysupply(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    priority_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'common_plysupply'


class CommonPlysupplyrequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'common_plysupplyrequest'


class CommonPlytype(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
   # shape = models.PolygonField(
       # srid=28992,
       # default=None,
       # null=True,
       # blank=True,
       # help_text=translate("polygon of ply as in the nest (inserted with the right x,y,angle)"),
   # )  # This field type is a guess.
    shape = models.TextField()  # This field type is a guess.
    max_tray_filling_count = models.IntegerField()
    min_iou = models.FloatField()
    pressure_pick = models.FloatField()
    pressure_move = models.FloatField()
    extra_fields = models.JSONField(blank=True, null=True)
    max_ply_supply_filling_count = models.IntegerField()
    material = models.ForeignKey(CommonMaterial, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_plytype'
        unique_together = (('name', 'material'),)


class CommonProcess(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    chosen_strategy = models.ForeignKey('CommonStrategy', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_process'


class CommonProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    sequence_num = models.IntegerField()
    state = models.CharField(max_length=20)
    product_definition = models.ForeignKey('CommonProductdefinition', models.DO_NOTHING, blank=True, null=True)
    workorder = models.ForeignKey('CommonWorkorder', models.DO_NOTHING)
    end_destination = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_product'
        unique_together = (('sequence_num', 'workorder'),)


class CommonProductdefinition(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    max_tray_filling_count = models.IntegerField()
    process = models.ForeignKey(CommonProcess, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_productdefinition'


class CommonProductdefinitionfilling(models.Model):
    id = models.BigAutoField(primary_key=True)
    sequence = models.IntegerField()
    plytype = models.ForeignKey(CommonPlytype, models.DO_NOTHING)
    product_definition = models.ForeignKey(CommonProductdefinition, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_productdefinitionfilling'


class CommonProductfilling(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_ply_added = models.DateTimeField(blank=True, null=True)
    layer = models.IntegerField()
    zone = models.CharField(max_length=20)
    place_position_x = models.FloatField()
    place_position_y = models.FloatField()
    place_angle = models.FloatField()
    vacuum_zone_ids = models.TextField()  # This field type is a guess.
    state = models.CharField(max_length=20)
    ply = models.OneToOneField(CommonPly, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(CommonProduct, models.DO_NOTHING)
    product_definition_filling = models.ForeignKey(CommonProductdefinitionfilling, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_productfilling'


class CommonRejectionrequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    object_id = models.IntegerField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_rejectionrequest'


class CommonRoll(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    batch_id = models.CharField(max_length=200)
    roll_id = models.CharField(max_length=200)
    material = models.ForeignKey(CommonMaterial, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_roll'


class CommonSensor(models.Model):
    id = models.BigAutoField(primary_key=True)
    sensor_id = models.IntegerField()
    center_x = models.FloatField()
    center_y = models.FloatField()
    radius = models.FloatField()
    ee = models.ForeignKey(CommonEndeffector, models.DO_NOTHING)
    sc_id = models.ForeignKey('CommonSuctioncup', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_sensor'
        unique_together = (('sensor_id', 'ee'),)


class CommonStrategy(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    process_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'common_strategy'


class CommonSuctioncup(models.Model):
    id = models.BigAutoField(primary_key=True)
    suction_cup_id = models.IntegerField()
    center_x = models.FloatField()
    center_y = models.FloatField()
    radius = models.FloatField()
    ee = models.ForeignKey(CommonEndeffector, models.DO_NOTHING)
    activateable = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'common_suctioncup'
        unique_together = (('suction_cup_id', 'ee'),)


class CommonTableweldinstruction(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_welded = models.DateTimeField(blank=True, null=True)
    table_active_welding_unit_ids = models.TextField()  # This field type is a guess.
    state = models.CharField(max_length=20)
    product_filling = models.ForeignKey(CommonProductfilling, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_tableweldinstruction'


class CommonTask(models.Model):
    id = models.BigAutoField(primary_key=True)
    subsystem = models.CharField(max_length=200)
    command = models.IntegerField()
    data = models.JSONField(blank=True, null=True)
    uuid = models.UUIDField(unique=True)
    state = models.CharField(max_length=20)
    date_created = models.DateTimeField()
    date_started = models.DateTimeField(blank=True, null=True)
    date_rejected_canceled = models.DateTimeField(blank=True, null=True)
    date_done = models.DateTimeField(blank=True, null=True)
    task_flow = models.JSONField()
    strategy = models.ForeignKey(CommonStrategy, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_task'


class CommonTray(models.Model):
    id = models.BigAutoField(primary_key=True)
    buffer = models.ForeignKey(CommonBuffer, models.DO_NOTHING)
    reserved_ply_type = models.ForeignKey(CommonPlytype, models.DO_NOTHING, blank=True, null=True)
    reserved_product_definition = models.ForeignKey(CommonProductdefinition, models.DO_NOTHING, blank=True, null=True)
    reserved_sequence_nr = models.IntegerField(blank=True, null=True)
    reserved_product = models.ForeignKey(CommonProduct, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_tray'


class CommonTrayfilling(models.Model):
    id = models.BigAutoField(primary_key=True)
    sequence = models.IntegerField()
    ply = models.OneToOneField(CommonPly, models.DO_NOTHING, blank=True, null=True)
    product = models.OneToOneField(CommonProduct, models.DO_NOTHING, blank=True, null=True)
    tray = models.ForeignKey(CommonTray, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_trayfilling'
        unique_together = (('tray', 'sequence'),)


class CommonTrayrequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    buffer = models.ForeignKey(CommonBuffer, models.DO_NOTHING)
    tray = models.OneToOneField(CommonTray, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_trayrequest'


class CommonWeldingtable(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    priority_num = models.IntegerField(unique=True)
    active_product = models.ForeignKey(CommonProduct, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_weldingtable'


class CommonWeldingunit(models.Model):
    id = models.BigAutoField(primary_key=True)
    welding_unit_id = models.IntegerField()
    center_x = models.FloatField()
    center_y = models.FloatField()
    radius = models.FloatField()
    ee = models.ForeignKey(CommonEndeffector, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_weldingunit'
        unique_together = (('welding_unit_id', 'ee'),)


class CommonWeldinstruction(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_welded = models.DateTimeField(blank=True, null=True)
    ee_active_welding_unit_ids = models.TextField()  # This field type is a guess.
    weld_point_x = models.FloatField()
    weld_point_y = models.FloatField()
    weld_point_a = models.FloatField()
    state = models.CharField(max_length=20)
    product_filling = models.ForeignKey(CommonProductfilling, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'common_weldinstruction'


class CommonWorkorder(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    uuid = models.UUIDField(unique=True)
    date_created = models.DateTimeField()
    date_started = models.DateTimeField(blank=True, null=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=20)
    data = models.JSONField()
    process = models.ForeignKey(CommonProcess, models.DO_NOTHING, blank=True, null=True)
    required_ee = models.ForeignKey(CommonEndeffector, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'common_workorder'


class County(models.Model):
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    countyns = models.CharField(max_length=8, blank=True, null=True)
    cntyidfp = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    csafp = models.CharField(max_length=3, blank=True, null=True)
    cbsafp = models.CharField(max_length=5, blank=True, null=True)
    metdivfp = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'county'


class CountyLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)  # The composite primary key (st_code, co_code) found, that is not supported. The first column is selected.
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'county_lookup'
        unique_together = (('st_code', 'co_code'),)


class CountysubLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)  # The composite primary key (st_code, co_code, cs_code) found, that is not supported. The first column is selected.
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField()
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countysub_lookup'
        unique_together = (('st_code', 'co_code', 'cs_code'),)


class Cousub(models.Model):
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    cousubfp = models.CharField(max_length=5, blank=True, null=True)
    cousubns = models.CharField(max_length=8, blank=True, null=True)
    cosbidfp = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    cnectafp = models.CharField(max_length=3, blank=True, null=True)
    nectafp = models.CharField(max_length=5, blank=True, null=True)
    nctadvfp = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.DecimalField(max_digits=14, decimal_places=0, blank=True, null=True)
    awater = models.DecimalField(max_digits=14, decimal_places=0, blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'cousub'


class DirectionLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    abbrev = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'direction_lookup'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Edges(models.Model):
    gid = models.AutoField(primary_key=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    tfidl = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tfidr = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    smid = models.CharField(max_length=22, blank=True, null=True)
    lfromadd = models.CharField(max_length=12, blank=True, null=True)
    ltoadd = models.CharField(max_length=12, blank=True, null=True)
    rfromadd = models.CharField(max_length=12, blank=True, null=True)
    rtoadd = models.CharField(max_length=12, blank=True, null=True)
    zipl = models.CharField(max_length=5, blank=True, null=True)
    zipr = models.CharField(max_length=5, blank=True, null=True)
    featcat = models.CharField(max_length=1, blank=True, null=True)
    hydroflg = models.CharField(max_length=1, blank=True, null=True)
    railflg = models.CharField(max_length=1, blank=True, null=True)
    roadflg = models.CharField(max_length=1, blank=True, null=True)
    olfflg = models.CharField(max_length=1, blank=True, null=True)
    passflg = models.CharField(max_length=1, blank=True, null=True)
    divroad = models.CharField(max_length=1, blank=True, null=True)
    exttyp = models.CharField(max_length=1, blank=True, null=True)
    ttyp = models.CharField(max_length=1, blank=True, null=True)
    deckedroad = models.CharField(max_length=1, blank=True, null=True)
    artpath = models.CharField(max_length=1, blank=True, null=True)
    persist = models.CharField(max_length=1, blank=True, null=True)
    gcseflg = models.CharField(max_length=1, blank=True, null=True)
    offsetl = models.CharField(max_length=1, blank=True, null=True)
    offsetr = models.CharField(max_length=1, blank=True, null=True)
    tnidf = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    tnidt = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'edges'


class Faces(models.Model):
    gid = models.AutoField(primary_key=True)
    tfid = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    statefp00 = models.CharField(max_length=2, blank=True, null=True)
    countyfp00 = models.CharField(max_length=3, blank=True, null=True)
    tractce00 = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce00 = models.CharField(max_length=1, blank=True, null=True)
    blockce00 = models.CharField(max_length=4, blank=True, null=True)
    cousubfp00 = models.CharField(max_length=5, blank=True, null=True)
    submcdfp00 = models.CharField(max_length=5, blank=True, null=True)
    conctyfp00 = models.CharField(max_length=5, blank=True, null=True)
    placefp00 = models.CharField(max_length=5, blank=True, null=True)
    aiannhfp00 = models.CharField(max_length=5, blank=True, null=True)
    aiannhce00 = models.CharField(max_length=4, blank=True, null=True)
    comptyp00 = models.CharField(max_length=1, blank=True, null=True)
    trsubfp00 = models.CharField(max_length=5, blank=True, null=True)
    trsubce00 = models.CharField(max_length=3, blank=True, null=True)
    anrcfp00 = models.CharField(max_length=5, blank=True, null=True)
    elsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    scsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    unsdlea00 = models.CharField(max_length=5, blank=True, null=True)
    uace00 = models.CharField(max_length=5, blank=True, null=True)
    cd108fp = models.CharField(max_length=2, blank=True, null=True)
    sldust00 = models.CharField(max_length=3, blank=True, null=True)
    sldlst00 = models.CharField(max_length=3, blank=True, null=True)
    vtdst00 = models.CharField(max_length=6, blank=True, null=True)
    zcta5ce00 = models.CharField(max_length=5, blank=True, null=True)
    tazce00 = models.CharField(max_length=6, blank=True, null=True)
    ugace00 = models.CharField(max_length=5, blank=True, null=True)
    puma5ce00 = models.CharField(max_length=5, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce = models.CharField(max_length=1, blank=True, null=True)
    blockce = models.CharField(max_length=4, blank=True, null=True)
    cousubfp = models.CharField(max_length=5, blank=True, null=True)
    submcdfp = models.CharField(max_length=5, blank=True, null=True)
    conctyfp = models.CharField(max_length=5, blank=True, null=True)
    placefp = models.CharField(max_length=5, blank=True, null=True)
    aiannhfp = models.CharField(max_length=5, blank=True, null=True)
    aiannhce = models.CharField(max_length=4, blank=True, null=True)
    comptyp = models.CharField(max_length=1, blank=True, null=True)
    trsubfp = models.CharField(max_length=5, blank=True, null=True)
    trsubce = models.CharField(max_length=3, blank=True, null=True)
    anrcfp = models.CharField(max_length=5, blank=True, null=True)
    ttractce = models.CharField(max_length=6, blank=True, null=True)
    tblkgpce = models.CharField(max_length=1, blank=True, null=True)
    elsdlea = models.CharField(max_length=5, blank=True, null=True)
    scsdlea = models.CharField(max_length=5, blank=True, null=True)
    unsdlea = models.CharField(max_length=5, blank=True, null=True)
    uace = models.CharField(max_length=5, blank=True, null=True)
    cd111fp = models.CharField(max_length=2, blank=True, null=True)
    sldust = models.CharField(max_length=3, blank=True, null=True)
    sldlst = models.CharField(max_length=3, blank=True, null=True)
    vtdst = models.CharField(max_length=6, blank=True, null=True)
    zcta5ce = models.CharField(max_length=5, blank=True, null=True)
    tazce = models.CharField(max_length=6, blank=True, null=True)
    ugace = models.CharField(max_length=5, blank=True, null=True)
    puma5ce = models.CharField(max_length=5, blank=True, null=True)
    csafp = models.CharField(max_length=3, blank=True, null=True)
    cbsafp = models.CharField(max_length=5, blank=True, null=True)
    metdivfp = models.CharField(max_length=5, blank=True, null=True)
    cnectafp = models.CharField(max_length=3, blank=True, null=True)
    nectafp = models.CharField(max_length=5, blank=True, null=True)
    nctadvfp = models.CharField(max_length=5, blank=True, null=True)
    lwflag = models.CharField(max_length=1, blank=True, null=True)
    offset = models.CharField(max_length=1, blank=True, null=True)
    atotal = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    tractce20 = models.CharField(max_length=6, blank=True, null=True)
    blkgrpce20 = models.CharField(max_length=1, blank=True, null=True)
    blockce20 = models.CharField(max_length=4, blank=True, null=True)
    countyfp20 = models.CharField(max_length=3, blank=True, null=True)
    statefp20 = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faces'


class Featnames(models.Model):
    gid = models.AutoField(primary_key=True)
    tlid = models.BigIntegerField(blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    predirabrv = models.CharField(max_length=15, blank=True, null=True)
    pretypabrv = models.CharField(max_length=50, blank=True, null=True)
    prequalabr = models.CharField(max_length=15, blank=True, null=True)
    sufdirabrv = models.CharField(max_length=15, blank=True, null=True)
    suftypabrv = models.CharField(max_length=50, blank=True, null=True)
    sufqualabr = models.CharField(max_length=15, blank=True, null=True)
    predir = models.CharField(max_length=2, blank=True, null=True)
    pretyp = models.CharField(max_length=3, blank=True, null=True)
    prequal = models.CharField(max_length=2, blank=True, null=True)
    sufdir = models.CharField(max_length=2, blank=True, null=True)
    suftyp = models.CharField(max_length=3, blank=True, null=True)
    sufqual = models.CharField(max_length=2, blank=True, null=True)
    linearid = models.CharField(max_length=22, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    paflag = models.CharField(max_length=1, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'featnames'


class GeocodeSettings(models.Model):
    name = models.TextField(primary_key=True)
    setting = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    short_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geocode_settings'


class GeocodeSettingsDefault(models.Model):
    name = models.TextField(primary_key=True)
    setting = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    short_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geocode_settings_default'


class KittingRecipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    name = models.CharField(unique=True, max_length=100)
    ee = models.ForeignKey(CommonEndeffector, models.DO_NOTHING, blank=True, null=True)
    process = models.ForeignKey(CommonProcess, models.DO_NOTHING, to_field='name')

    class Meta:
        managed = False
        db_table = 'kitting_recipe'


class Layer(models.Model):
    topology = models.OneToOneField('Topology', models.DO_NOTHING, primary_key=True)  # The composite primary key (topology_id, layer_id) found, that is not supported. The first column is selected.
    layer_id = models.IntegerField()
    schema_name = models.CharField(max_length=50)
    table_name = models.CharField(max_length=50)
    feature_column = models.CharField(max_length=50)
    feature_type = models.IntegerField()
    level = models.IntegerField()
    child_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'layer'
        unique_together = (('topology', 'layer_id'), ('schema_name', 'table_name', 'feature_column'),)


class LoaderLookuptables(models.Model):
    process_order = models.IntegerField()
    lookup_name = models.TextField(primary_key=True, db_comment='This is the table name to inherit from and suffix of resulting output table -- how the table will be named --  edges here would mean -- ma_edges , pa_edges etc. except in the case of national tables. national level tables have no prefix')
    table_name = models.TextField(blank=True, null=True, db_comment='suffix of the tables to load e.g.  edges would load all tables like *edges.dbf(shp)  -- so tl_2010_42129_edges.dbf .  ')
    single_mode = models.BooleanField()
    load = models.BooleanField(db_comment="Whether or not to load the table.  For states and zcta5 (you may just want to download states10, zcta510 nationwide file manually) load your own into a single table that inherits from tiger.states, tiger.zcta5.  You'll get improved performance for some geocoding cases.")
    level_county = models.BooleanField()
    level_state = models.BooleanField()
    level_nation = models.BooleanField(db_comment='These are tables that contain all data for the whole US so there is just a single file')
    post_load_process = models.TextField(blank=True, null=True)
    single_geom_mode = models.BooleanField(blank=True, null=True)
    insert_mode = models.CharField(max_length=1)
    pre_load_process = models.TextField(blank=True, null=True)
    columns_exclude = models.TextField(blank=True, null=True, db_comment='List of columns to exclude as an array. This is excluded from both input table and output table and rest of columns remaining are assumed to be in same order in both tables. gid, geoid,cpi,suffix1ce are excluded if no columns are specified.')  # This field type is a guess.
    website_root_override = models.TextField(blank=True, null=True, db_comment='Path to use for wget instead of that specified in year table.  Needed currently for zcta where they release that only for 2000 and 2010')

    class Meta:
        managed = False
        db_table = 'loader_lookuptables'


class LoaderPlatform(models.Model):
    os = models.CharField(primary_key=True, max_length=50)
    declare_sect = models.TextField(blank=True, null=True)
    pgbin = models.TextField(blank=True, null=True)
    wget = models.TextField(blank=True, null=True)
    unzip_command = models.TextField(blank=True, null=True)
    psql = models.TextField(blank=True, null=True)
    path_sep = models.TextField(blank=True, null=True)
    loader = models.TextField(blank=True, null=True)
    environ_set_command = models.TextField(blank=True, null=True)
    county_process_command = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loader_platform'


class LoaderVariables(models.Model):
    tiger_year = models.CharField(primary_key=True, max_length=4)
    website_root = models.TextField(blank=True, null=True)
    staging_fold = models.TextField(blank=True, null=True)
    data_schema = models.TextField(blank=True, null=True)
    staging_schema = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loader_variables'


class NestMovementDetectionLidarconfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    lidars_on = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nest_movement_detection_lidarconfig'


class NestMovementDetectionNestmovementresult(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    reference = models.JSONField(blank=True, null=True)
    intermediate = models.JSONField(blank=True, null=True)
    ply = models.OneToOneField(CommonPly, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nest_movement_detection_nestmovementresult'


class PagcGaz(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'pagc_gaz'


class PagcLex(models.Model):
    seq = models.IntegerField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)
    stdword = models.TextField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)
    is_custom = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'pagc_lex'


class PagcRules(models.Model):
    rule = models.TextField(blank=True, null=True)
    is_custom = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagc_rules'


class Place(models.Model):
    statefp = models.CharField(max_length=2, blank=True, null=True)
    placefp = models.CharField(max_length=5, blank=True, null=True)
    placens = models.CharField(max_length=8, blank=True, null=True)
    plcidfp = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=100, blank=True, null=True)
    namelsad = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    classfp = models.CharField(max_length=2, blank=True, null=True)
    cpi = models.CharField(max_length=1, blank=True, null=True)
    pcicbsa = models.CharField(max_length=1, blank=True, null=True)
    pcinecta = models.CharField(max_length=1, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.BigIntegerField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'place'


class PlaceLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)  # The composite primary key (st_code, pl_code) found, that is not supported. The first column is selected.
    state = models.CharField(max_length=2, blank=True, null=True)
    pl_code = models.IntegerField()
    name = models.CharField(max_length=90, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'place_lookup'
        unique_together = (('st_code', 'pl_code'),)


class PlyInspectionInspectionconfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=200)
    inspection_on = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ply_inspection_inspectionconfig'


class PlyInspectionInspectionresult(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField()
    success = models.BooleanField()
    inspection_dx = models.FloatField()
    inspection_dy = models.FloatField()
    inspection_da = models.FloatField()
    intersection_over_union = models.FloatField()
    ply_contours = models.JSONField(blank=True, null=True)
    design_contours = models.JSONField(blank=True, null=True)
    marker_positions = models.JSONField(blank=True, null=True)
    marker_positions_empty_ee = models.JSONField(blank=True, null=True)
    ply = models.OneToOneField(CommonPly, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ply_inspection_inspectionresult'


class PlyInspectionTcpcalibration(models.Model):
    id = models.BigAutoField(primary_key=True)
    state = models.CharField(max_length=20)
    date_started = models.DateTimeField()
    date_step1_complete = models.DateTimeField(blank=True, null=True)
    date_step2_complete = models.DateTimeField(blank=True, null=True)
    date_finished = models.DateTimeField(blank=True, null=True)
    date_aborted = models.DateTimeField(blank=True, null=True)
    tcp_offset_x = models.FloatField(blank=True, null=True)
    tcp_offset_y = models.FloatField(blank=True, null=True)
    tcp_angle = models.FloatField(blank=True, null=True)
    field_marker_loc_empty_ee = models.JSONField(db_column='_marker_loc_empty_ee', blank=True, null=True)  # Field renamed because it started with '_'.
    field_marker_loc_step1 = models.JSONField(db_column='_marker_loc_step1', blank=True, null=True)  # Field renamed because it started with '_'.
    field_marker_loc_step2 = models.JSONField(db_column='_marker_loc_step2', blank=True, null=True)  # Field renamed because it started with '_'.
    field_marker_loc_step3 = models.JSONField(db_column='_marker_loc_step3', blank=True, null=True)  # Field renamed because it started with '_'.
    field_tcp_offset_x_error = models.FloatField(db_column='_tcp_offset_x_error', blank=True, null=True)  # Field renamed because it started with '_'.
    field_tcp_offset_y_error = models.FloatField(db_column='_tcp_offset_y_error', blank=True, null=True)  # Field renamed because it started with '_'.
    field_tcp_angle_error = models.FloatField(db_column='_tcp_angle_error', blank=True, null=True)  # Field renamed because it started with '_'.
    field_tcp_offset_rot_avg = models.FloatField(db_column='_tcp_offset_rot_avg', blank=True, null=True)  # Field renamed because it started with '_'.
    field_tcp_offset_rot_error = models.FloatField(db_column='_tcp_offset_rot_error', blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'ply_inspection_tcpcalibration'


class PreformingRecipe(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    date_created = models.DateTimeField()
    ee = models.ForeignKey(CommonEndeffector, models.DO_NOTHING, blank=True, null=True)
    process = models.ForeignKey(CommonProcess, models.DO_NOTHING, to_field='name')

    class Meta:
        managed = False
        db_table = 'preforming_recipe'


class SecondaryUnitLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=20)
    abbrev = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'secondary_unit_lookup'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class State(models.Model):
    region = models.CharField(max_length=2, blank=True, null=True)
    division = models.CharField(max_length=2, blank=True, null=True)
    statefp = models.CharField(primary_key=True, max_length=2)
    statens = models.CharField(max_length=8, blank=True, null=True)
    stusps = models.CharField(unique=True, max_length=2)
    name = models.CharField(max_length=100, blank=True, null=True)
    lsad = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.BigIntegerField(blank=True, null=True)
    awater = models.BigIntegerField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'state'


class StateLookup(models.Model):
    st_code = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=40, blank=True, null=True)
    abbrev = models.CharField(unique=True, max_length=3, blank=True, null=True)
    statefp = models.CharField(unique=True, max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'state_lookup'


class StreetTypeLookup(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    abbrev = models.CharField(max_length=50, blank=True, null=True)
    is_hw = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'street_type_lookup'


class Tabblock(models.Model):
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blockce = models.CharField(max_length=4, blank=True, null=True)
    tabblock_id = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=20, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    ur = models.CharField(max_length=1, blank=True, null=True)
    uace = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tabblock'


class Tabblock20(models.Model):
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    blockce = models.CharField(max_length=4, blank=True, null=True)
    geoid = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=10, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    ur = models.CharField(max_length=1, blank=True, null=True)
    uace = models.CharField(max_length=5, blank=True, null=True)
    uatype = models.CharField(max_length=1, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tabblock20'


class Topology(models.Model):
    name = models.CharField(unique=True, max_length=50)
    srid = models.IntegerField()
    precision = models.FloatField()
    hasz = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'topology'


class Tract(models.Model):
    statefp = models.CharField(max_length=2, blank=True, null=True)
    countyfp = models.CharField(max_length=3, blank=True, null=True)
    tractce = models.CharField(max_length=6, blank=True, null=True)
    tract_id = models.CharField(primary_key=True, max_length=11)
    name = models.CharField(max_length=7, blank=True, null=True)
    namelsad = models.CharField(max_length=20, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tract'


class Zcta5(models.Model):
    statefp = models.CharField(max_length=2)
    zcta5ce = models.CharField(primary_key=True, max_length=5)  # The composite primary key (zcta5ce, statefp) found, that is not supported. The first column is selected.
    classfp = models.CharField(max_length=2, blank=True, null=True)
    mtfcc = models.CharField(max_length=5, blank=True, null=True)
    funcstat = models.CharField(max_length=1, blank=True, null=True)
    aland = models.FloatField(blank=True, null=True)
    awater = models.FloatField(blank=True, null=True)
    intptlat = models.CharField(max_length=11, blank=True, null=True)
    intptlon = models.CharField(max_length=12, blank=True, null=True)
    partflg = models.CharField(max_length=1, blank=True, null=True)
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'zcta5'
        unique_together = (('zcta5ce', 'statefp'),)


class ZipLookup(models.Model):
    zip = models.IntegerField(primary_key=True)
    st_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField(blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField(blank=True, null=True)
    cousub = models.CharField(max_length=90, blank=True, null=True)
    pl_code = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=90, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup'


class ZipLookupAll(models.Model):
    zip = models.IntegerField(blank=True, null=True)
    st_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.IntegerField(blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    cs_code = models.IntegerField(blank=True, null=True)
    cousub = models.CharField(max_length=90, blank=True, null=True)
    pl_code = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=90, blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup_all'


class ZipLookupBase(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)
    state = models.CharField(max_length=40, blank=True, null=True)
    county = models.CharField(max_length=90, blank=True, null=True)
    city = models.CharField(max_length=90, blank=True, null=True)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_lookup_base'


class ZipState(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)  # The composite primary key (zip, stusps) found, that is not supported. The first column is selected.
    stusps = models.CharField(max_length=2)
    statefp = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zip_state'
        unique_together = (('zip', 'stusps'),)


class ZipStateLoc(models.Model):
    zip = models.CharField(primary_key=True, max_length=5)  # The composite primary key (zip, stusps, place) found, that is not supported. The first column is selected.
    stusps = models.CharField(max_length=2)
    statefp = models.CharField(max_length=2, blank=True, null=True)
    place = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'zip_state_loc'
        unique_together = (('zip', 'stusps', 'place'),)
