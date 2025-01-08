{
    'name': 'Hotel Management System',
    'version': '1.0',
    'summary': 'Module hotel management system',
    'description': """
        Module management hotel:
        - Manage hotel and room
        - Manage room feature
        - Manage booking
        - Manager and staff roles
    """,
    'author': 'Lee',
    'website': 'https://ahtgroup.com',
    'category': 'Management',
    'depends': ['base','hr'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rule_hotel.xml',
        'security/record_rule_room.xml',
        'security/record_rule_booking.xml',
        'views/hotel_view.xml',
        'views/room_view.xml',
        'views/room_feature.xml',
        'views/booking_view.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'icon': '/hotel_management/static/description/icon.png',
}