"""
Add Job Management Navigation Items for RPO_Admin
This script adds the new job service layer navigation items to the RPO_Admin menu
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import NavigationItem, NavigationGroup

def add_job_management_nav():
    """Add job management navigation items for RPO_Admin"""
    
    print("=" * 60)
    print("Adding Job Management Navigation for RPO_Admin")
    print("=" * 60)
    
    # Check existing items
    existing = NavigationItem.objects.filter(
        url_name__in=[
            'App:job_list_view',
            'App:employer_dashboard_view',
            'App:job_create_view',
            'App:job_analytics_view',
        ]
    )
    
    if existing.exists():
        print(f"\n⚠️  Found {existing.count()} existing job management items:")
        for item in existing:
            print(f"   - {item.title} ({item.url_name})")
            roles = item.visible_to_roles if isinstance(item.visible_to_roles, list) else []
            if 'rpo_admin' not in roles:
                roles.append('rpo_admin')
                item.visible_to_roles = roles
                item.save()
                print(f"     ✅ Added 'rpo_admin' to visible roles")
            else:
                print(f"     ℹ️  Already visible to rpo_admin")
        print("\n✨ Updated existing items!")
        return
    
    # Find the highest order number for RPO_Admin items
    rpo_items = [i for i in NavigationItem.objects.filter(is_active=True) 
                 if 'rpo_admin' in (i.visible_to_roles if isinstance(i.visible_to_roles, list) else [])]
    max_order = max([item.order for item in rpo_items], default=0) if rpo_items else 5
    
    print(f"\n📊 Current max order for RPO_Admin items: {max_order}")
    print(f"📝 Starting new items at order: {max_order + 1}")
    
    # Navigation items to add
    nav_items = [
        {
            'title': 'Job Management',
            'url_name': 'App:employer_dashboard_view',
            'icon': 'fa-solid fa-briefcase',
            'order': max_order + 1,
            'visible_to_roles': ['rpo_admin', 'hiring_manager'],
            'description': 'Manage job postings and applications'
        },
        {
            'title': 'Browse All Jobs',
            'url_name': 'App:job_list_view',
            'icon': 'fa-solid fa-list',
            'order': max_order + 2,
            'visible_to_roles': ['rpo_admin', 'hiring_manager', 'candidate'],
            'description': 'View all active job listings'
        },
        {
            'title': 'Post New Job',
            'url_name': 'App:job_create_view',
            'icon': 'fa-solid fa-plus-circle',
            'order': max_order + 3,
            'visible_to_roles': ['rpo_admin', 'hiring_manager'],
            'description': 'Create new job posting'
        },
        {
            'title': 'Job Analytics',
            'url_name': 'App:job_analytics_view',
            'icon': 'fa-solid fa-chart-line',
            'order': max_order + 4,
            'visible_to_roles': ['rpo_admin', 'hiring_manager'],
            'description': 'View job posting statistics and analytics'
        },
    ]
    
    # Create navigation items
    created_count = 0
    for item_data in nav_items:
        # Check if already exists
        existing = NavigationItem.objects.filter(
            url_name=item_data['url_name']
        ).first()
        
        if existing:
            print(f"\n⚠️  Item already exists: {item_data['title']}")
            # Update roles if needed
            roles = existing.visible_to_roles if isinstance(existing.visible_to_roles, list) else []
            updated = False
            for role in item_data['visible_to_roles']:
                if role not in roles:
                    roles.append(role)
                    updated = True
            
            if updated:
                existing.visible_to_roles = roles
                existing.save()
                print(f"   ✅ Updated visible roles: {roles}")
            else:
                print(f"   ℹ️  No changes needed")
            continue
        
        # Create new item
        item = NavigationItem.objects.create(
            title=item_data['title'],
            url_name=item_data['url_name'],
            icon=item_data['icon'],
            order=item_data['order'],
            visible_to_roles=item_data['visible_to_roles'],
            is_active=True,
            group=None,  # No group for now
            parent=None,  # Top-level items
        )
        
        print(f"\n✅ Created: {item.title}")
        print(f"   URL: {item.url_name}")
        print(f"   Icon: {item.icon}")
        print(f"   Order: {item.order}")
        print(f"   Roles: {', '.join(item.visible_to_roles)}")
        
        created_count += 1
    
    print("\n" + "=" * 60)
    print(f"✨ Successfully added {created_count} navigation items!")
    print("=" * 60)
    
    # Display current RPO_Admin menu
    print("\n📋 Current RPO_Admin Navigation Menu:")
    print("-" * 60)
    rpo_items = sorted(
        [i for i in NavigationItem.objects.filter(is_active=True) 
         if 'rpo_admin' in (i.visible_to_roles if isinstance(i.visible_to_roles, list) else [])],
        key=lambda x: x.order
    )
    
    for idx, item in enumerate(rpo_items, 1):
        print(f"{idx}. [{item.order}] {item.title}")
        print(f"   URL: {item.url_name}")
        print(f"   Icon: {item.icon or 'None'}")
        print(f"   Roles: {', '.join(item.visible_to_roles)}")
        print()
    
    print("=" * 60)
    print("🎉 Job Management navigation added successfully!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("1. Restart your Django server")
    print("2. Login as rpo_admin user")
    print("3. Check the navigation menu for new items")
    print("\n💡 Note: Make sure you've added the URL configuration:")
    print("   path('jobs/', include('App.urls_job_management'))")
    print("   to your main urls.py file")
    print("=" * 60)


if __name__ == '__main__':
    try:
        add_job_management_nav()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
