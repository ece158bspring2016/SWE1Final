//
//  ViewController.swift
//  ECE158BFinal
//
//  Created by Max X on 5/6/16.
//  Copyright © 2016 Max Xing. All rights reserved.
//


import UIKit


class LocationsViewController: UITableViewController {
    
    
    var passName:String!
   // var locations:[Location] = LocationsData
    var locations:[Location]! = []

  
    override func viewDidLoad() {
        super.viewDidLoad()
            
        getData()
            
        self.tableView.delegate = self
        self.tableView.dataSource = self
            
        self.tableView.contentInset = UIEdgeInsetsMake(20, 0, 0, 0);
            
            
        }

    func getData(){
        
        let myRootRef = Firebase(url:"https://ece158final.firebaseio.com")
        
        myRootRef.queryOrderedByChild("Name").observeEventType(.ChildAdded, withBlock: { snapshot in
            if let name = snapshot.value["Name"] as? String {
                print("\(snapshot.key) was \(name) name")
                self.locations.append(Location(name:name))
                print("data size is ", self.locations.count)
            }
            
            
            dispatch_async(dispatch_get_main_queue(), { () -> Void in
                self.tableView.reloadData()
            })
            
        })
    }

    
    
    
    // MARK: - Table view data source
    
    override func numberOfSectionsInTableView(tableView: UITableView) -> Int {
        return 1
    }
    
    override func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return locations.count
    }
    
    override func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath)
        -> UITableViewCell {
            let cell = tableView.dequeueReusableCellWithIdentifier("LocationTableViewCell", forIndexPath: indexPath)
            
            let loc = locations[indexPath.row] as Location
            cell.textLabel?.text = loc.name
           // cell.detailTextLabel?.text = String(loc.rating)
            return cell
    }
    
    
    override func tableView(tableView: UITableView, didSelectRowAtIndexPath indexPath: NSIndexPath) {
        
        // Get Cell Label
        let indexPath = tableView.indexPathForSelectedRow;
        let currentCell = tableView.cellForRowAtIndexPath(indexPath!) as UITableViewCell!;
        
        passName = currentCell.textLabel!.text!
        performSegueWithIdentifier("showDetail", sender: self)

    }
    
    
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?){
        if (segue.identifier == "showDetail") {
       
            let viewController = segue.destinationViewController as! DetailViewController
            // your new view controller should have property that will store passed value
            viewController.name = passName
        }
    }
    
}


