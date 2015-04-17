from scoring.check import Check
import sys

def checkOnce(master, team_id, service_id):
    conn = master.db.conn
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()

    """ Don't hate me pls, for some reason 'SELECT * FROM services WHERE id = %s' doesnt work """
    query = "SELECT * FROM services WHERE id = " + str(service_id)
    cursor1.execute(query)
    row = cursor1.fetchone()

    if row is not None:
        service_id = row[0]
        service_name = row[1]
        module = row[2]
    
        cursor2.execute("SELECT `value` FROM services_data WHERE team_id = %s AND service_id = %s ORDER BY `order` ASC", (team_id, service_id))
    
        args = []
        data = cursor2.fetchone()
    
        while data is not None:
            args.append(data[0])
        
            data = cursor2.fetchone()
    else:
        sys.exit("[FAIL] Service ID does not exist")

    cursor1.close()
    cursor2.close()

    module = master.config['scripts'] % (module)
    check = Check(master, team_id, service_id, "", module, args)
    (status, output) = check.main(addLog=False, addScore=False)

    print output
    print "Status: " + ("PASS" if status == 0 else "FAIL")