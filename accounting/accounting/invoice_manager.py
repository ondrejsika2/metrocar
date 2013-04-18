def do_something(sender, **kwargs):    
    obj = kwargs['instance']
    from metrocar.utils.log import get_logger
    get_logger().info("invoice instance id="+ str(obj.id) +" deleted from admin")