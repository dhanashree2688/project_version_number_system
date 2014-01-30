#!C:/Python26/python.exe
import web
db = web.database(dbn='mysql', user='root', pw='', db='test')
from web import form

render = web.template.render('templates/')

urls = ('/', 'front', '/admin', 'admin', '/manage', 'manage', '/privilege', 'privilege', '/passe', 'passe', '/create', 'create', '/login', 'login', '/index', 'index', '/add', 'add', '/edit', 'edit', '/display', 'display', '/CookieGet', 'CookieGet')

class front:
    def GET(self):
        f = db.select('users')
	return render.front(f)
class login:
	def GET(self):
		log = db.select('users')
		i = db.select('version_table')
		j = db.select('version_table')
		k = db.select('build_table')
		l = db.select('project_type')
		#return render.index(i, j, k, l)
		return render.login(log)
		
		#web.render('index.html')
		
	def POST(self): 
		x = web.input()
		vars = dict(u = x.username,p = x.password)
		user = x.username
		passwd = x.password
		m = db.query("select userid from users where username = $u and password = $p",vars=dict(u=x.username,p=x.password))
		web.setcookie("username", x.username, 3600)
		n = db.query("select userid from users where username = $u and password = $p and role = 'admin'",vars=dict(u=x.username,p=x.password))
		#if n:
		#if (user!='super' and passwd!='super'):
			#return "valid user"
		#	raise web.seeother("http://127.0.0.1:8080/index")				
		#if(user == 'super' and passwd == 'super'):
		if n:
			#return "No such user exists"
			raise web.seeother("http://127.0.0.1:8080/admin")
			#raise web.seeother('/')
		if m:
			raise web.seeother("http://127.0.0.1:8080/index")
		else:
			raise web.seeother('/')
class index: 
	def GET(self): 
			i = db.select('version_table')
			j = db.select('version_table')
			k = db.select('build_table')
			l = db.select('project_type')
			return render.index(i, j, k, l)        
class add:
    def POST(self):
        x = web.input()
        n = db.insert('version_table',project_name=x.project_name, major_version=x.major_version, minor_version=x.minor_version, bugfix_version=x.bugfix_version, build_number=x.build_number)
        raise web.seeother('/')	
        
class edit:
	def GET(self): 
			i = db.select('version_table')
			return render.index(i)
	def POST(self):
        	x = web.input()
        	vars = dict(p = x.project_name)
	       	m = x.changes  
	       	y = x.proj_types
	        if (m == 'major_version' and y == 'component'):
	        	n = db.query("update version_table set major_version = major_version+1, minor_version = 0, bugfix_version = 0, build_number = build_number+1 where project_name = $p",vars=dict(p=x.project_name))
	        if (m == 'minor_version' and y == 'component'):
	        	n = db.query("update version_table set minor_version = minor_version+1, build_number = build_number+1, bugfix_version = 0 where project_name = $p",vars=dict(p=x.project_name))
	        if (m == 'bugfix_version'and y == 'component'):
	        	n = db.query("update version_table set bugfix_version = bugfix_version+1, build_number = build_number+1 where project_name = $p",vars=dict(p=x.project_name))
	       	if (m == 'build_number'and y == 'component'):
	        	n = db.query("update version_table set build_number = build_number+1 where project_name = $p",vars=dict(p=x.project_name))
		if (m == 'bugfix_version' and y == 'installer'):
			n = db.query("update version_table set bugfix_version = bugfix_version+1 where project_name = $p",vars=dict(p=x.project_name))
		if (m == 'build_number' and y == 'installer'):
			n = db.query("update version_table set build_number = build_number+1 where project_name = $p",vars=dict(p=x.project_name))
		if n:
			raise web.seeother("http://127.0.0.1:8080/display")
	              
	        #raise web.seeother('/')
class display:
	def GET(self):
			dis = db.select('version_table')
			return render.display(dis)
	
	def POST(self):
		x = web.input()
		vars = dict(p = x.project_name)
		#n = db.query("select version_no from version_table where project_name = $p",vars=dict(p=x.project_name))
		if n:
			raise web.seeother("http://127.0.0.1:8080/CookieGet")
class CookieGet:
    def GET(self):
	try: 
             return "The user who checked out the latest version is: " + web.cookies().username
        except:
            return "Cookie does not exist."
class admin:
	def GET(self):
		ad = db.select('admin_choice')
		return render.admin(ad)
	def POST(self):
		x = web.input()
		#y = x.functions
				

class manage:
	def GET(self):
		mng = db.select('users')
		return render.manage(mng)
	def POST(self):
		x = web.input()
		#self.y = x.username
		web.setcookie("username", x.username, 3600)
		#y = x.functions
		raise web.seeother("http://127.0.0.1:8080/privilege")
		
class create:
	def POST(self):
		x = web.input()
		n = db.insert('users',username=x.username,password=x.password)
		#self.z = x.username
		web.setcookie("username", x.username, 3600)
		raise web.seeother("http://127.0.0.1:8080/privilege")
			
class privilege:
	def GET(self):
		#prv = db.query("select userid from users where username = x.username")
		#n = db.query("select userid from users where username = web.cookies().username")
		prv = db.select('users')
		#form.Show(web.cookies().username, description="Username")
		return render.privilege(prv)
	def POST(self):
		x = web.input()
		vars = dict(p = x.username)
		#form.Textbox("web.cookies().username", description="Username")
		#n = db.query("select userid from users where username = web.cookies().username")
		n = db.query("update users set role = 'admin' where username = $p",vars=dict(p=x.username))
		raise web.seeother('/')
class passe:
	def GET(self):
		pas = db.select('users')
		return render.passe(pas)
	def POST(self):
		x = web.input()
		u = web.cookies().username
		vars = dict(p = x.password,u = web.cookies().username)
		n = db.query("update users set password = $p where username = $u",vars=dict(p=x.password,u = web.cookies().username))
		raise web.seeother('/')
	
	

if __name__=="__main__":
    web.internalerror = web.debugerror
    app = web.application(urls, globals())
    app.run()