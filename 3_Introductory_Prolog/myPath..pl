% Author: Tingshan Yu
% Date: 2014/10/18
%-------------------------------------------------------------------------------
% Input the all edges below
arc(a,b,10).
arc(a,e,2).
arc(a,d,10).
arc(e,b,1).
arc(d,e,1).
arc(b,c,3).
arc(b,f,6).
arc(e,f,7).
arc(d,f,6).
arc(f,c,2).
arc(c,g,4).
arc(f,g,1).
%-------------------------------------------------------------------------------
% Make sure that M and N is connected.
connected(M,N,Weight):-arc(M,N,Weight).

% Find all paths from A to B, output the Cost and Path at the same time
find(X,X,[0,[X]]).
find(X,Y,[Cost,[X|Path]]):-connected(X,Z,Wt),find(Z,Y,[Cost0,Path]),Cost is Cost0 + Wt.

% Put all found Cost&Path into a list. The minimum element in the list is the result.
path(A,B,P):-bagof(Cost_Path,find(A,B,Cost_Path),CPList),min_member(P,CPList).