;; major mode for the ally programming language

(defvar ally-events
  '("var"
	"pred"
	"func"
	"ctrl"
	"return"
	))

(defvar ally-keywords
  '("module"
	"def"
	))

(defvar ally-indent-offset 4
  "*Indentation offset for `ally-mode'.")

(defun current-line ()
  "Return the vertical position of point..."
  (+ (count-lines (window-start) (point))
	 (if (= (current-column) 0) 1 0)))

;; swiped from python mode
(defun ally-indent-region (start end)                                                            
  "`indent-region-function' for Ally.                                                            
Leaves validly-indented lines alone, i.e. doesn't indent to                                        
another valid position."                                                                           
  (save-excursion                                                                                  
    (goto-char end)                                                                                
    (setq end (point-marker))                                                                      
    (goto-char start)                                                                              
    (or (bolp) (forward-line 1))                                                                   
    (while (< (point) end)                                                                         
	  (beginning-of-line)
	  (ally-indent-line)
	  (ally-indent-line)
	  (end-of-line)
	  (ally-indent-line)
	  (ally-indent-line)
	  (beginning-of-line)
	  (ally-indent-line)
	  (ally-indent-line)
      (forward-line 1))
    (move-marker end nil)))

;; thanks 
;; http://stackoverflow.com/questions/4158216/emacs-custom-indentation
;; @ scottfrazer
(defun ally-indent-line ()
  "Indent current line for `ally-mode'."
  (interactive)
  (let ((indent-col 0)
		(pipe-col 0)
		)	
    (save-excursion
      (beginning-of-line)
      (condition-case nil
          (while t
            (backward-up-list 1)
            (when (looking-at "[[{]")
              (setq indent-col (+ indent-col ally-indent-offset))))
        (error nil)))

    (save-excursion	;; first day elisp, so it's a little rough I bet.
	  (let ((done nil)
			(pipe-loc nil))
		(while (not done)		  
		  (backward-char 1)		
		  (when (looking-at "{")
			(setq done t))		  		 		  
		  (when (looking-at "}")
			(setq done t))		  		 		  
		  (when (looking-at ";")
			(setq done t))		  
		  (when (looking-at "|")
			(when (not done)
			  (setq done t)
			  (setq pipe-loc (current-column))
			  (setq indent-col pipe-loc)))		 
		  )))

    (save-excursion
      (back-to-indentation)
      (when (and (looking-at "[]}]") (>= indent-col ally-indent-offset))
        (setq indent-col (- indent-col ally-indent-offset))))
	
    (indent-line-to indent-col)))

(defvar ally-tab-width 4 "Width of a tab for ALLY mode")

;; Two small edits.
;; First is to put an extra set of parens () around the list
;; which is the format that font-lock-defaults wants
;; Second, you used ' (quote) at the outermost level where you wanted ` (backquote)
;; you were very close


(defvar ally-font-lock-defaults
  `((
	 ;; stuff between "
	 ;("\"\\.\\*\\?" . font-lock-string-face)
	 ;("\`\\.\\*\\?" . font-lock-string-face)	 
	 
	 (">" . font-lock-keyword-face)
	 ("<" . font-lock-keyword-face)
	 ("|" . font-lock-type-face)
	 ("+" . font-lock-string-face)
	 ("=" . font-lock-builtin-face)
	 ("-" . font-lock-warning-face)
	 (";" . font-lock-comment-delimiter-face)
	 ( ,(regexp-opt ally-keywords 'words) . font-lock-builtin-face)
	 ( ,(regexp-opt ally-events 'words) . font-lock-constant-face)
	 )))
  
;(define-derived-mode foo-mode text-mode "Foo"
;  "Mode for editing some kind of config files."
;  (make-local-variable 'foo-indent-offset)
;  (set (make-local-variable 'indent-line-function) 'foo-indent-line))


(define-derived-mode ally-mode c-mode "Ally script"
  "Ally mode is a major mode for editing .ally files"
    
  ;; you again used quote when you had '((ally-hilite))
  ;; I just updated the variable to have the proper nesting (as noted above)
  ;; and use the value directly here
  (setq font-lock-defaults ally-font-lock-defaults)
  
  ;; when there's an override, use it
  ;; otherwise it gets the default value
  (when ally-tab-width
	(setq tab-width ally-tab-width))
  
  ;; for comments
  ;; overriding these vars gets you what (I think) you want
  ;; they're made buffer local when you set them
  ;;(setq comment-start "//")
  ;;(setq comment-end "")

  (make-local-variable 'ally-indent-offset)
  (make-local-variable 'ally-indent-buffer)

  ;;(set (make-local-variable 'comment-start) comment-start)
  ;;(set (make-local-variable 'comment-end) comment-end)
  (set (make-local-variable 'indent-line-function) 'ally-indent-line)
  (set (make-local-variable 'indent-region-function) #'ally-indent-region)
  ;(set (make-local-variable 'indent-region-function) #'ally-indent-buffer)
  

  (modify-syntax-entry ?# "< b" ally-mode-syntax-table)
  (modify-syntax-entry ?\n "> b" ally-mode-syntax-table)
  ;;A gnu-correct program will have some sort of hook call here.
  (c-toggle-electric-state -1)
  )

(provide 'ally-mode)