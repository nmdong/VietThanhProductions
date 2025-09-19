//
//  TableView+Extension.swift
//  RaoVat
//
//  Created by Admin on 11/16/22.
//

import Foundation
import UIKit
import CRRefresh
import SnapKit

public extension UITableView {

    /// SwifterSwift: Number of all rows in all sections of tableView.
    ///
    /// - Returns: The count of all rows in the tableView.
    func numberOfRows() -> Int {
        var section = 0
        var rowCount = 0
        while section < numberOfSections {
            rowCount += numberOfRows(inSection: section)
            section += 1
        }
        return rowCount
    }

    /// SwifterSwift: IndexPath for last row in section.
    ///
    /// - Parameter section: section to get last row in.
    /// - Returns: optional last indexPath for last row in section (if applicable).
    func indexPathForLastRow(inSection section: Int) -> IndexPath? {
        guard numberOfSections > 0, section >= 0 else { return nil }
        guard numberOfRows(inSection: section) > 0  else {
            return IndexPath(row: 0, section: section)
        }
        return IndexPath(row: numberOfRows(inSection: section) - 1, section: section)
    }

    /// Reload data with a completion handler.
    ///
    /// - Parameter completion: completion handler to run after reloadData finishes.
    func reloadData(_ completion: @escaping () -> Void) {
        UIView.animate(withDuration: 0, animations: {
            self.reloadData()
        }, completion: { _ in
            completion()
        })
    }

    /// SwifterSwift: Remove TableFooterView.
    func removeTableFooterView() {
        tableFooterView = nil
    }

    /// SwifterSwift: Remove TableHeaderView.
    func removeTableHeaderView() {
        tableHeaderView = nil
    }


    /// SwifterSwift: Dequeue reusable UITableViewCell using class name
    ///
    /// - Parameter name: UITableViewCell type
    /// - Returns: UITableViewCell object with associated class name.
    func dequeueReusableCell<T: UITableViewCell>(withClass name: T.Type) -> T {
        guard let cell = dequeueReusableCell(withIdentifier: String(describing: name)) as? T else {
            fatalError("Couldn't find UITableViewCell for \(String(describing: name)), make sure the cell is registered with table view")
        }
        return cell
    }

    /// SwifterSwift: Dequeue reusable UITableViewCell using class name for indexPath
    ///
    /// - Parameters:
    ///   - name: UITableViewCell type.
    ///   - indexPath: location of cell in tableView.
    /// - Returns: UITableViewCell object with associated class name.
    func dequeueReusableCell<T: UITableViewCell>(withClass name: T.Type, for indexPath: IndexPath) -> T {
        guard let cell = dequeueReusableCell(withIdentifier: String(describing: name), for: indexPath) as? T else {
            fatalError("Couldn't find UITableViewCell for \(String(describing: name)), make sure the cell is registered with table view")
        }
        return cell
    }


    /// SwifterSwift: Register UITableViewHeaderFooterView using class name
    ///
    /// - Parameters:
    ///   - nib: Nib file used to create the header or footer view.
    ///   - name: UITableViewHeaderFooterView type.
    func register<T: UITableViewHeaderFooterView>(nib: UINib?, withHeaderFooterViewClass name: T.Type) {
        register(nib, forHeaderFooterViewReuseIdentifier: String(describing: name))
    }

    /// SwifterSwift: Register UITableViewHeaderFooterView using class name
    ///
    /// - Parameter name: UITableViewHeaderFooterView type
    func register<T: UITableViewHeaderFooterView>(headerFooterViewClassWith name: T.Type) {
        register(T.self, forHeaderFooterViewReuseIdentifier: String(describing: name))
    }

    /// SwifterSwift: Register UITableViewCell using class name
    ///
    /// - Parameter name: UITableViewCell type
    func register<T: UITableViewCell>(cellWithClass name: T.Type) {
        register(T.self, forCellReuseIdentifier: String(describing: name))
    }

    /// SwifterSwift: Register UITableViewCell using class name
    ///
    /// - Parameters:
    ///   - nib: Nib file used to create the tableView cell.
    ///   - name: UITableViewCell type.
    func register<T: UITableViewCell>(nib: UINib?, withCellClass name: T.Type) {
        register(nib, forCellReuseIdentifier: String(describing: name))
    }

    /// SwifterSwift: Register UITableViewCell with .xib file using only its corresponding class.
    ///               Assumes that the .xib filename and cell class has the same name.
    ///
    /// - Parameters:
    ///   - name: UITableViewCell type.
    ///   - bundleClass: Class in which the Bundle instance will be based on.
    func register<T: UITableViewCell>(nibWithCellClass name: T.Type, at bundleClass: AnyClass? = nil) {
        let identifier = String(describing: name)
        var bundle: Bundle?

        if let bundleName = bundleClass {
            bundle = Bundle(for: bundleName)
        }

        register(UINib(nibName: identifier, bundle: bundle), forCellReuseIdentifier: identifier)
    }
}
public extension UIScrollView {
        
    func crHeadRefresh(completion: @escaping(()->Void)) {
        self.cr.addHeadRefresh(animator: FastAnimator()) {
            completion()
        }
    }
    
    func crFootRefresh(completion: @escaping(()->Void)) {
        self.cr.addFootRefresh(animator: FastAnimator()) {
            completion()
        }
    }
    
    func updateRefreshStatus(_ currentPage : Int, totalPage : Int) {
        if currentPage == totalPage {
            self.cr.noticeNoMoreData()
            self.cr.footer?.isHidden = true
        } else {
            self.cr.resetNoMore()
            if currentPage == 1 {
                self.cr.footer?.isHidden = false
            }
        }
    }
    
    func isHasMoreData(_ moreData : Bool) {
        if !moreData {
            self.cr.noticeNoMoreData()
            self.cr.footer?.isHidden = true
        } else {
            self.cr.resetNoMore()
            self.cr.footer?.isHidden = false
        }
    }
    
    func crEndRefresh() {
        DispatchQueue.main.async {
            self.cr.endHeaderRefresh()
            self.cr.endLoadingMore()
        }
    }
}
extension UITableView {
   
    func setupEmptyView(){
        guard let emptyView = self.backgroundView as? EmptyView else {
            let view = EmptyView.loadFromNib(named: EmptyView.className) as! EmptyView
            self.backgroundView = view
            view.snp.makeConstraints { (make) in
                make.width.height.equalToSuperview()
            }
            view.isHidden = true
            return
        }
        emptyView.isHidden = true
    }
    
    func setupEmptyView(_ title : String?, desc : String?) {
        guard let emptyView = self.backgroundView as? EmptyView else {
            let view = EmptyView.loadFromNib(named: EmptyView.className) as! EmptyView
            self.backgroundView = view
            view.snp.makeConstraints { (make) in
                make.width.height.equalToSuperview()
            }
            view.isHidden = true
            view.setuiWithTitle(title, desc: desc)
            return
        }
        emptyView.isHidden = true
        emptyView.backgroundColor = .clear
        emptyView.setuiWithTitle(title, desc: desc)
    }
    
    func showEmptyView(_ show : Bool, message : String? = nil) {
        guard let emptyView = self.backgroundView  as? EmptyView else {return}
        emptyView.isHidden = !show
        if let _message = message {
            emptyView.lbTitle.text = _message
        }
    }
}

extension UICollectionView {
    func registerNibWithName(_ name : String) {
        self.register(UINib.init(nibName: name, bundle: nil), forCellWithReuseIdentifier: name)
    }
    
    
    func setupEmptyView(){
        guard let emptyView = self.backgroundView as? EmptyView else {
            let view = EmptyView.loadFromNib(named: EmptyView.className) as! EmptyView
            self.backgroundView = view
            view.snp.makeConstraints { (make) in
                make.width.height.equalToSuperview()
            }
            view.isHidden = true
            return
        }
        emptyView.isHidden = true
    }
    
    func setupEmptyView(_ title : String?, desc : String?) {
        guard let emptyView = self.backgroundView as? EmptyView else {
            let view = EmptyView.loadFromNib(named: EmptyView.className) as! EmptyView
            self.backgroundView = view
            view.snp.makeConstraints { (make) in
                make.width.height.equalToSuperview()
            }
            view.isHidden = true
            view.setuiWithTitle(title, desc: desc)
            return
        }
        emptyView.backgroundColor = .clear
        emptyView.isHidden = true
        emptyView.setuiWithTitle(title, desc: desc)
    }
    
    func showEmptyView(_ show : Bool, message : String? = nil) {
        guard let emptyView = self.backgroundView  as? EmptyView else {return}
        emptyView.isHidden = !show
        if let _message = message {
            emptyView.lbTitle.text = _message
        }
    }
}

public extension UIView {
    class func loadFromNib(named name: String, bundle: Bundle? = nil) -> UIView? {
        return UINib(nibName: name, bundle: bundle).instantiate(withOwner: nil, options: nil)[0] as? UIView
    }
}

extension NSObject {
    var className: String {
        return String(describing: type(of: self))
    }
    
    class var className: String {
        return String(describing: self)
    }
}
